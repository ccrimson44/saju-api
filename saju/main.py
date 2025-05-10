from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GPTRequest(BaseModel):
    saju_text: str
    question: str

@app.post("/ask-gpt")
async def ask_gpt(data: GPTRequest):
    prompt = (
        f"당신은 한국 사주 전문가입니다.\n\n"
        f"■ 사용자 사주 정보:\n{data.saju_text}\n\n"
        f"■ 질문:\n{data.question}\n\n"
        f"위 정보를 바탕으로 전문가처럼 진지하고 정확하게 조언해 주세요."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 한국 사주 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85
        )
        result = response.choices[0].message["content"]
        return Response(
            content=json.dumps({"answer": result}, ensure_ascii=False),
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        return Response(
            content=json.dumps({"answer": f"오류 발생: {str(e)}"}, ensure_ascii=False),
            media_type="application/json; charset=utf-8"
        )

@app.get("/debug/openai-key")
def debug_openai_key():
    api_key = os.getenv("OPENAI_API_KEY", "❌ 환경변수 없음")
    masked_key = api_key[:5] + "..." + api_key[-4:] if "sk-" in api_key else api_key
    return {"OPENAI_API_KEY": masked_key}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("saju.main:app", host="0.0.0.0", port=port)
