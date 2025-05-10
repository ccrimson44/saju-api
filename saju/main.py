from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import openai

# 환경 변수에서 OpenAI 키 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS 설정 (FlutterFlow에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에선 특정 도메인으로 제한 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 사주 분석 요청 데이터 모델
class AnalyzeRequest(BaseModel):
    year: int
    month: int
    day: int
    time: str  # 예: 오전 11시
    type: str  # 양력 / 음력

# GPT 질문 요청 데이터 모델
class AskRequest(BaseModel):
    saju_text: str
    question: str

# 응답 모델
class AnswerResponse(BaseModel):
    answer: str

# 사주 분석 엔드포인트
@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    formatted = f"당신은 {req.type} 기준으로 {req.year}년 {req.month}월 {req.day}일 {req.time}에 태어났습니다."
    return {"result": formatted}

# GPT 응답 생성 엔드포인트
@app.post("/ask-gpt", response_model=AnswerResponse)
async def ask_gpt(req: AskRequest):
    try:
        prompt = (
            f"[사주 정보]\n{req.saju_text}\n\n"
            f"[사용자 질문]\n{req.question}\n\n"
            f"위 사주와 질문에 근거하여 전문적인 사주 코치처럼 조언해 주세요."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 사주 전문가입니다. 친절하고 현실적인 조언을 제공하세요."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = completion.choices[0].message["content"]
        return {"answer": answer}

    except Exception as e:
        return {"answer": f"오류 발생: \n{str(e)}"}

# Render 배포를 위한 실행 설정
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("saju.main:app", host="0.0.0.0", port=port)
