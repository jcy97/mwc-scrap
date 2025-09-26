import uvicorn
from main import app
from init_db import setup_database

if __name__ == "__main__":
    print("전시회 규칙 관리 시스템을 시작합니다...")

    print("1. 데이터베이스 설정 중...")
    setup_database()

    print("2. 웹 서버를 시작합니다...")
    print("브라우저에서 http://localhost:8000 을 열어주세요.")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
