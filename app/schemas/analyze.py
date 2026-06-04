from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    message: str


class ScoredMessage(BaseModel):
    time: str
    sender: str = ""
    message: str = ""
    score: int = 0
    dimension: str = ""
    reason: str = ""


class KlineRequest(BaseModel):
    messages: list[ScoredMessage]


class IndexPoint(BaseModel):
    time: str
    index: int


class KlineBar(BaseModel):
    date: str
    open: int
    high: int
    low: int
    close: int


class GenerateKlineResponse(BaseModel):
    messages: list[ScoredMessage]
    index: list[IndexPoint]
    kline: list[KlineBar]


class ExportRequest(BaseModel):
    messages: list[ScoredMessage]
    index: list[IndexPoint]
    kline: list[KlineBar]
