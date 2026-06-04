from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router
from app.api.export import router as export_router
from app.api.kline import router as kline_router
from app.api.upload import router as upload_router

app = FastAPI(title="Love Kline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(kline_router)
app.include_router(export_router)


@app.get("/")
def root():
    return {"message": "Love Kline is running"}
