from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import openai

# 환경변수에서 OpenAI API 키 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS 설정 (FlutterFlow 등 외부 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 시엔 보안 위해 출처 제한 필요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ▶︎ 사주 분석 요청 바디
class AnalyzeRequest(BaseModel):
    year: int
    month: int
    day: int
    time: str  # "오전 11시" 같은 문자열
    type: str  # "양력" 또는 "음력"

# ▶︎ GPT 질문 요청 바디
class AskRequest(BaseModel):
    saju_text: str
    question: str

# ▶︎ GPT 응답 반환 형식
class AnswerResponse(BaseModel):
    answer: str

# 🔹 사주 정보 텍스트 생성 API
@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    formatted = f"당신은 {req.type} 기준으로 {req.year}년 {req.month}월 {req.day}일 {req.time}에 태어났습니다."
    return JSONResponse(content={"result": formatted}, media_type="application/json; charset=utf-8")

# 🔹 GPT 응답 생성 API
@app.post("/ask-gpt", response_model=AnswerResponse)
async def ask_gpt(req: AskRequest):
    try:
        prompt = (
            f"[사주 정보]\n{req.saju_text}\n\n"
            f"[사용자 질문]\n{req.question}\n\n"
            f"위 사주와 질문에 근거하여 전문적인 사주 코치처럼 조언해 주세요."
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 사주 전문가입니다. 친절하고 현실적인 조언을 제공합니다."},
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message["content"]
        return JSONResponse(content={"answer": answer}, media_type="application/json; charset=utf-8")

    except Exception as e:
        return JSONResponse(content={"answer": f"오류 발생: \n{str(e)}"}, media_type="application/json; charset=utf-8")

# 🔹 로컬 및 Render 호환 실행 설정
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render에서는 환경 변수 PORT를 사용
    uvicorn.run("saju.main:app", host="0.0.0.0", port=port)
