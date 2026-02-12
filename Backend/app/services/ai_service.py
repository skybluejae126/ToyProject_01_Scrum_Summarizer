import google.generativeai as genai
from app.config import settings, logger

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        logger.info("Gemini AI 모델 연결 완료")

    async def summarize(self, text: str, user_template: str):
        prompt = f"""
        당신은 회의 요약 전문가입니다. 아래의 [스크럼 전사본]을 분석하여 
        사용자가 요청한 [양식]에 맞춰 정리하세요.
        
        [양식]: {user_template}
        [스크럼 전사본]: {text}
        
        결과는 반드시 Notion에 바로 붙여넣을 수 있도록 깔끔한 Markdown 형식을 사용하세요.
        """
        try:
            logger.debug("Gemini 요약 프로세스 시작")
            response = self.model.generate_content(prompt)
            logger.success("Gemini 요약본 생성 성공")
            return response.text
        except Exception as e:
            logger.error(f"Gemini API 호출 실패: {e}")
            raise e