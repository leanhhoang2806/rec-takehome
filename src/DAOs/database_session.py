from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.configs.config import CONFIG


class Database:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False
        )

    def get_session(self) -> Session:
        db = self.SessionLocal()
        try:
            return db
        finally:
            db.close()


db = Database(CONFIG.POSTGRES_DATABASE_URL_CONNECTION_STRING)
session = db.get_session()
