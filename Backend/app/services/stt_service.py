import torch
from transformers import pipeline
from app.config import logger
import librosa

class STTService:
    def __init__(self):
        logger.info("STT 파이프라인(Whisper) 초기화 중...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        #Transformers를 이용한 Whisper 호출
        self.asr_pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-large-v3", # 성능을 위해 large-v3 권장
            device=self.device
        )
        logger.success(f"STT 서비스 로드 완료 (Device: {self.device})")

    async def transcribe(self, audio_path: str):
        logger.debug(f"파일 분석 시작: {audio_path}")
        try:
            # 오디오 로드 및 전사
            result = self.asr_pipe(audio_path, generate_kwargs={"language": "korean"})
            text = result["text"]
            logger.info(f"전사 결과 추출 성공: {text[:50]}...")
            return text
        except Exception as e:
            logger.error(f"전사 중 오류 발생: {str(e)}")
            raise e