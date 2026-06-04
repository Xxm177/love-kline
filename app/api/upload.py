from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from app.services.parser import parse_chat

router = APIRouter()

@router.post("/upload")
async def upload_file(
        file:UploadFile = File(...)
):
    content = await file.read()
    text = content.decode("utf-8")
    messages = parse_chat(text)

    return{
        "count":len(messages),
        "messages":messages
    }