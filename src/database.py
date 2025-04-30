from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

from src.config import config

sqlite_args = {
    "connect_args": {"check_same_thread": False},
    "poolclass": StaticPool
}

engine_kwargs = {}

if config.DB_URL.startswith("sqlite"):
    engine_kwargs = sqlite_args

engine = create_engine(str(config.DB_URL), **engine_kwargs)
SessionFactory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
