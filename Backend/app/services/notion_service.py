from notion_client import Client, APIResponseError
from app.config import settings, logger
from datetime import datetime

class NotionService:
    def __init__(self):
        self.notion = Client(auth=settings.NOTION_TOKEN)

    async def create_scrum_page(self, summary_text: str):
        try:
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            safe_content = summary_text[:1900] + "..." if len(summary_text) > 2000 else summary_text

            logger.info("노션 페이지 생성을 시도합니다...")
            
            new_page = self.notion.pages.create(
                parent={"database_id": settings.NOTION_DATABASE_ID.strip()},
                properties={
                    # 1. '강의 노트'가 제목(Title) 유형이므로 여기에 제목을 넣습니다.
                    "강의 노트": {
                        "title": [{"text": {"content": f"🚀 스크럼 요약 ({date_str})"}}]
                    },
                    # 2. '작성 날짜'가 날짜(Date) 유형이므로 여기에 날짜를 넣습니다.
                    "작성 날짜": {
                        "date": {"start": datetime.now().date().isoformat()}
                    },
                    # (선택) '강의명' 컬럼에 프로젝트 이름을 넣고 싶다면?
                    # 만약 '강의명'이 선택(Select) 유형이라면 아래와 같이 추가 가능합니다.
                    "강의명": {
                        "select": {"name": "스크럼"} 
                    }
                },
                children=[
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {"rich_text": [{"text": {"content": "📝 AI 요약 결과"}}]}
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": safe_content}}]
                        }
                    }
                ]
            )
            logger.success(f"노션 기록 성공! URL: {new_page['url']}")
            return new_page['url']

        except APIResponseError as e:
            # e.message 대신 str(e) 사용
            logger.error(f"노션 API 응답 에러: {str(e)}")
            logger.warning("도움말: 노션 DB의 컬럼 이름이 'Name'과 'Date'가 맞는지 꼭 확인하세요!")
            raise e
        except Exception as e:
            logger.error(f"예상치 못한 노션 에러: {str(e)}")
            raise e