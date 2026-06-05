import threading

from fastapi import APIRouter, File, UploadFile

from app.schemas.analyze import (
    GenerateKlineResponse,
    KlineRequest,
)
from app.services.deepseek import score_messages_batch
from app.services.kline_generator import generate_kline
from app.services.parser import parse_chat
from app.services.relation import build_relation_index
from app.services import task_manager

router = APIRouter()


@router.post("/kline")
def create_kline(data: KlineRequest) -> dict:
    messages = [m.model_dump() for m in data.messages]
    index_data = build_relation_index(messages)
    kline_data = generate_kline(index_data)
    return {"index": index_data, "kline": kline_data}


@router.post("/generate-kline", response_model=GenerateKlineResponse)
async def generate_kline_full(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    text = content.decode("utf-8")
    parsed = parse_chat(text)

    # Batch score all messages
    message_texts = [m["message"] for m in parsed]
    scores = score_messages_batch(message_texts)

    # Merge parsed messages with scores
    scored_messages: list[dict] = []
    for i, msg in enumerate(parsed):
        s = scores[i] if i < len(scores) else {"score": 0, "dimension": "", "reason": ""}
        scored_messages.append({
            "time": msg["time"],
            "sender": msg["sender"],
            "message": msg["message"],
            "score": s["score"],
            "dimension": s["dimension"],
            "reason": s["reason"],
        })

    # Build relation index
    index_data = build_relation_index(scored_messages)

    # Generate K-line
    kline_data = generate_kline(index_data)

    return {
        "messages": scored_messages,
        "index": index_data,
        "kline": kline_data,
    }


def _process_in_background(task_id: str, text: str):
    try:
        parsed = parse_chat(text)
        if not parsed:
            task_manager.set_error(task_id, "无法解析聊天记录，请检查格式")
            return

        message_texts = [m["message"] for m in parsed]
        total = len(message_texts)

        def _progress(cur: int, tot: int):
            task_manager.update_progress(task_id, cur, tot)

        scores = score_messages_batch(message_texts, on_progress=_progress)

        scored = []
        for i, msg in enumerate(parsed):
            s = scores[i] if i < len(scores) else {"score": 0, "dimension": "", "reason": ""}
            scored.append({
                "time": msg["time"],
                "sender": msg["sender"],
                "message": msg["message"],
                "score": s["score"],
                "dimension": s["dimension"],
                "reason": s["reason"],
            })

        idx = build_relation_index(scored)
        kl = generate_kline(idx)

        task_manager.set_done(task_id, {
            "messages": scored,
            "index": idx,
            "kline": kl,
        })
    except Exception as e:
        task_manager.set_error(task_id, str(e))


@router.post("/generate-kline-async")
async def generate_kline_async(file: UploadFile = File(...)) -> dict:
    content = await file.read()
    text = content.decode("utf-8")
    task_id = task_manager.create()

    thread = threading.Thread(
        target=_process_in_background,
        args=(task_id, text),
        daemon=True,
    )
    thread.start()

    return {"task_id": task_id}


@router.get("/task/{task_id}")
def get_task_status(task_id: str) -> dict:
    task = task_manager.get(task_id)
    if task is None:
        return {"status": "not_found", "error": "任务不存在或已过期"}
    return task
