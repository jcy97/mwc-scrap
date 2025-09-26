from models import init_database, get_session
from sqlalchemy import text


def setup_database():
    try:
        engine = init_database()
        print("데이터베이스 테이블이 성공적으로 생성되었습니다.")

        session = get_session()
        result = session.execute(
            text(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
        )
        tables = result.fetchall()

        print("생성된 테이블:")
        for table in tables:
            print(f"  - {table[0]}")

        session.close()

    except Exception as e:
        print(f"데이터베이스 설정 중 오류 발생: {str(e)}")
        print("config.py에서 데이터베이스 연결 정보를 확인해주세요.")


if __name__ == "__main__":
    setup_database()
