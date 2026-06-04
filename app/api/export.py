from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.analyze import ExportRequest
from app.services.exporter import export_to_excel

router = APIRouter()


@router.post("/export")
def export_excel(data: ExportRequest):
    buffer = export_to_excel(
        messages=[m.model_dump() for m in data.messages],
        index=[i.model_dump() for i in data.index],
        kline=[k.model_dump() for k in data.kline],
    )

    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=love_kline.xlsx"},
    )
