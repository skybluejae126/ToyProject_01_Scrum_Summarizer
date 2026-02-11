from fastapi import FastAPI, UploadFile, File, Form
from app.config import logger
from app.services.stt_service import STTService
from app.services.ai_service import AIService
import os

app = FastAPI()

# 서비스 초기화
stt_service = STTService()
ai_service = AIService()

@app.post("/api/v1/scrum")
async def process_scrum(
    file: UploadFile = File(...),
    template: str = Form("일일 스크럼 요약 양식")
):
    logger.info(f"요청 수신: {file.filename}")
    
    # 1. 파일 저장
    temp_path = f"uploads/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        # 2. STT 전사
        raw_text = await stt_service.transcribe(temp_path)
        
        # 3. AI 요약
        summary = await ai_service.summarize(raw_text, template)
        
        # 4. (추후 구현) Notion 기록 로직 호출...
        
        return {"status": "success", "summary": summary}
    
    except Exception as e:
        logger.exception("치명적 오류 발생")
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)