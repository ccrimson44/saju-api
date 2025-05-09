from fastapi import FastAPI, Request
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/analyze_saju")
async def analyze_saju(request: Request):
    data = await request.json()
    birth_info = data.get("birth_info", {})
    
    prompt = f"""
    다음은 사용자의 사주 정보입니다:
    - 생년: {birth_info.get('year')}
    - 생월: {birth_info.get('month')}
    - 생일: {birth_info.get('day')}
    - 생시: {birth_info.get('time')}
    - 양력/음력: {birth_info.get('type')}

    위 사주를 간단히 분석해줘.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 유능한 사주 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"result": completion.choices[0].message["content"]}
