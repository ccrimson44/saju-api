from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from .saju_logic import calculate_fake_saju
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    year: int
    month: int
    day: int
    time: str
    type: str

@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    result = calculate_fake_saju(req.year, req.month, req.day, req.time, req.type)

    # 수동으로 utf-8 인코딩된 JSON 응답 생성
    return Response(
        content=json.dumps({"result": result}, ensure_ascii=False),
        media_type="application/json; charset=utf-8"
    )
