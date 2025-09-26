import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "username")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "exhibition_rules")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

POSTGRES_HOST = DB_HOST
POSTGRES_PORT = DB_PORT
POSTGRES_DB = DB_NAME
POSTGRES_USER = DB_USER
POSTGRES_PASSWORD = DB_PASSWORD
