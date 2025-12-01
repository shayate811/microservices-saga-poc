from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. 環境変数から接続URLを取得
# docker-compose.ymlで設定した "DATABASE_URL" がここで読み込まれます
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. エンジンの作成
# echo=True にすると発行されるSQLがログに出るため、学習・デバッグに最適です
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 3. セッションの作成
# DBとの対話（CRUD）を行うためのクラス
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. ベースクラスの作成
# 今後作成するモデル（テーブル定義）はこれを継承します
Base = declarative_base()

# 5. DBセッションの依存性注入 (Dependency Injection)
# FastAPIのパス操作関数で 'db: Session = Depends(get_db)' として使います
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
