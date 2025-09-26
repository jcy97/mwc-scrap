# 전시회 규칙 관리 시스템

Mobile World Congress 전시회 규칙을 크롤링하여 체계적으로 관리하는 웹 애플리케이션입니다.

## 주요 기능

- 🕷️ **자동 크롤링**: 전시회 웹사이트에서 최신 규칙 자동 수집
- 📊 **데이터베이스 저장**: PostgreSQL에 체계적으로 분류하여 저장
- 🌐 **웹 인터페이스**: 직관적이고 아름다운 웹 인터페이스 제공
- 📄 **PDF 다운로드**: 전체 규칙을 예쁜 PDF 문서로 다운로드
- 📊 **PPT 다운로드**: 프레젠테이션용 PowerPoint 파일 생성
- 🔍 **카테고리별 정리**: 규칙을 주제별로 체계적 분류

## 크롤링 대상 URL

1. https://gsma.my.site.com/mwcoem/s/New%20for%202026
2. https://gsma.my.site.com/mwcoem/s/Event%20Rules%20and%20Regulations
3. https://gsma.my.site.com/mwcoem/s/Stand%20Build%20Rules%20and%20Regulations

## 설치 및 실행

### 1. Poetry 환경 설정

```bash
# Poetry 설치 (없을 경우)
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
poetry install
```

### 2. 데이터베이스 설정

`config.py` 파일에서 PostgreSQL 연결 정보를 수정하세요:

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/exhibition_rules"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_DB = "exhibition_rules"
POSTGRES_USER = "username"
POSTGRES_PASSWORD = "password"
```

### 3. 애플리케이션 실행

```bash
# Poetry 환경에서 실행
poetry run python run.py

# 또는 Poetry shell 활성화 후 실행
poetry shell
python run.py
```

### 4. 웹 인터페이스 접속

브라우저에서 `http://localhost:8000`을 열어주세요.

## 사용법

1. **크롤링 시작**: 메인 페이지의 "크롤링 시작" 버튼 클릭
2. **데이터 확인**: 크롤링 완료 후 규칙 목록 확인
3. **상세보기**: 각 규칙의 "상세보기" 버튼으로 자세한 내용 확인
4. **문서 다운로드**: PDF 또는 PPT 형태로 전체 규칙 다운로드

## 프로젝트 구조

```
sample/
├── config.py              # 설정 파일
├── models.py              # 데이터베이스 모델
├── crawler.py             # 웹 크롤러
├── main.py                # FastAPI 애플리케이션
├── report_generator.py    # PDF/PPT 생성기
├── init_db.py             # 데이터베이스 초기화
├── run.py                 # 애플리케이션 실행
├── templates/
│   ├── index.html         # 메인 페이지
│   └── rule_detail.html   # 상세 페이지
└── pyproject.toml         # Poetry 설정
```

## 데이터베이스 스키마

### exhibition_rules

- 전시회 규칙 문서 정보

### rule_categories

- 규칙 카테고리 (예: 부스관리, 안전규정 등)

### rule_items

- 개별 규칙 항목들

## 기술 스택

- **Backend**: FastAPI, SQLAlchemy
- **Database**: PostgreSQL
- **Crawling**: Requests, BeautifulSoup4
- **Document Generation**: ReportLab, python-pptx
- **Frontend**: Bootstrap 5, Font Awesome
- **Package Management**: Poetry

## 주요 특징

- 반응형 웹 디자인
- 실시간 크롤링 상태 표시
- 카테고리별 체계적 분류
- 다국어 지원 준비
- 아름다운 UI/UX

## 문의사항

프로젝트 관련 문의사항이 있으시면 언제든지 연락주세요!
