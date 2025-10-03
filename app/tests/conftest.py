from __future__ import annotations
import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app as fastapi_app
from app.db.base import Base

from app.models import question as _question  # noqa: F401
from app.models import answer as _answer      # noqa: F401

# SQLite in-memory: общий инстанс для всех соединений
engine: Engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Включаем FK в SQLite
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def _get_test_db() -> Generator:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Подменяем зависимость БД у приложения
fastapi_app.dependency_overrides.clear()
from app.db.session import get_db  # импорт после fastapi_app, чтобы избежать циклов
fastapi_app.dependency_overrides[get_db] = _get_test_db

@pytest.fixture(autouse=True)
def _reset_db() -> Generator[None, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture()
def client() -> TestClient:
    return TestClient(fastapi_app)
