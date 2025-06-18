from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# .env読み込み
load_dotenv()

# 接続文字列
DATABASE_URL = os.getenv("DATABASE_URL")

# エンジン作成
engine = create_engine(DATABASE_URL)

# セッション
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseクラス（モデル定義用）
Base = declarative_base()
