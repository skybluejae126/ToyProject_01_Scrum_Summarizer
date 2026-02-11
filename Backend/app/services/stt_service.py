import torch
from transformers import pipeline
from app.config import logger
import librosa

class STTService:
    def __init__(self):
        logger.info("Whisper Pipeline 로딩 중...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.asr_pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base", # 속도를 위해 base 권장
            chunk_length_s=30,           # 30초 단위로 자동 분할 처리
            device=self.device
        )
        logger.success("STT 서비스 준비 완료")

    async def transcribe(self, audio_path: str):
        logger.info(f"긴 파일 전사 시작 (30s Chunking 모드): {audio_path}")
        try:
            # librosa로 전체를 읽지 않고 파일 경로를 직접 pipe에 전달
            # return_timestamps=True를 쓰면 구간별로 텍스트를 얻을 수 있음
            result = self.asr_pipe(
                audio_path, 
                batch_size=8, 
                return_timestamps=True,
                generate_kwargs={"language": "korean"}
            )
            
            # 전사된 전체 텍스트
            full_text = result["text"]
            logger.info("전체 전사 완료")
            return full_text
            
        except Exception as e:
            logger.error(f"전사 프로세스 중 치명적 오류: {e}")
            raise e