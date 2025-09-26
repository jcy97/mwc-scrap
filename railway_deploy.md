# Railway 배포 가이드

## 1. Railway 계정 생성

- https://railway.app 가입
- GitHub 연동

## 2. 프로젝트 준비

### Procfile 생성

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### requirements.txt 생성

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### 환경변수 설정 (Railway 대시보드에서)

```
DATABASE_URL=postgresql://user:password@host:port/database
DB_HOST=your_host
DB_PORT=5432
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database
```

## 3. 배포 명령어

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 생성 및 배포
railway init
railway up
```

## 4. PostgreSQL 데이터베이스

- Railway에서 PostgreSQL 플러그인 추가
- 자동으로 DATABASE_URL 환경변수 설정됨
