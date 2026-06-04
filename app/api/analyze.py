from fastapi import APIRouter

from app.schemas.analyze import AnalyzeRequest
from app.services.deepseek import score_message

router = APIRouter()

@router.post("/analyze")
def analyze(data: AnalyzeRequest):

    result = score_message(
        data.message
    )

    return result