from fastapi import APIRouter, File, UploadFile

from app.schemas.analyze import (
    GenerateKlineResponse,
    IndexPoint,
    KlineBar,
    KlineRequest,
    ScoredMessage,
)
from app.services.deepseek import score_messages_batch
from app.services.kline_generator import generate_kline
from app.services.parser import parse_chat
from app.services.relation import build_relation_index

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
