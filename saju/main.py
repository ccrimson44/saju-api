from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (FlutterFlow 또는 로컬 테스트를 위해 반드시 필요)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션 환경에서는 출처 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 형식 정의
class AnalyzeRequest(BaseModel):
    year: int
    month: int
    day: int
    time: str
    type: str  # "양력" 또는 "음력"

# 응답 형식 정의 (선택사항)
class AnalyzeResponse(BaseModel):
    result: str

# 엔드포인트 정의
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    # 간단한 분석 예시 (추후 사주 분석 로직으로 교체)
    formatted = f"{req.year}년 {req.month}월 {req.day}일 {req.time} ({req.type})"
    return {"result": f"분석된 결과: {formatted}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
