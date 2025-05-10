# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from saju_logic import calculate_fake_saju

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
    type: str  # 양력 or 음력

class AnalyzeResponse(BaseModel):
    result: str

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    result = calculate_fake_saju(req.year, req.month, req.day, req.time, req.type)
    return {"result": result}
