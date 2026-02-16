# 1. 베이스 이미지 설정 (Python 3.11 슬림 버전)
FROM python:3.11-slim

# 2. 시스템 의존성 설치 (FFmpeg는 soundfile/librosa 처리에 필수입니다)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. Pip 업그레이드 및 무거운 라이브러리(Torch) 우선 설치
# 이 부분을 따로 분리해야 코드가 수정되어도 Torch를 다시 다운로드하지 않습니다.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch==2.8.0 torchvision==0.23.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cu128

# 5. 나머지 의존성 설치
# requirements.txt에 soundfile과 librosa를 미리 넣어두는 것이 좋습니다.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. 소스 코드 복사
COPY . .

# 7. 서버 실행 (도커 환경에서는 --reload 대신 호스트 0.0.0.0 바인딩이 중요합니다)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]