# PostgreSQL 설치 및 설정 가이드

## 1. PostgreSQL 설치

### Homebrew 사용

```bash
brew install postgresql
brew services start postgresql
```

### 또는 Postgres.app 사용 (GUI)

- https://postgresapp.com/ 다운로드 후 설치

## 2. 데이터베이스 생성

```bash
# PostgreSQL 접속
psql postgres

# 사용자 생성
CREATE USER exhibition_user WITH PASSWORD 'exhibition_pass';

# 데이터베이스 생성
CREATE DATABASE exhibition_rules OWNER exhibition_user;

# 권한 부여
GRANT ALL PRIVILEGES ON DATABASE exhibition_rules TO exhibition_user;

# 종료
\q
```

## 3. .env 파일 수정

```env
DATABASE_URL=postgresql://exhibition_user:exhibition_pass@localhost:5432/exhibition_rules
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=exhibition_rules
POSTGRES_USER=exhibition_user
POSTGRES_PASSWORD=exhibition_pass
```

## 4. 테스트 연결

```bash
psql -h localhost -U exhibition_user -d exhibition_rules
```

## 5. 서버 재시작

```bash
# 현재 서버 중단 (Ctrl+C)
# 서버 재시작
poetry run python run.py
```
