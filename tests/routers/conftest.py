import os
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.configs import Settings, get_settings, ROOT_PATH
from app.db import get_db
from app.db.models import Base
from app.db.models.post import Post
from app.db.models.post_word import PostWord
from app.db.models.word import Word
from app.main import create_app
from app.utils.table_generator import create_tables

DB_FOLDER_PATH = os.path.join(ROOT_PATH, '.test_db')
os.makedirs(DB_FOLDER_PATH, exist_ok=True)

_engine = create_engine(f'sqlite:///{DB_FOLDER_PATH}/file.db')
_SessionLocal = sessionmaker(bind=_engine)


def local_get_db() -> Generator[Session, None, None]:
    with _SessionLocal() as db:
        yield db


def local_get_settings() -> Settings:
    return Settings(
        DB_DRIVER="dummy_driver",
        DB_HOST="dummy_host",
        DB_PORT=-1,
        DB_USER="dummy_user",
        DB_PASSWORD="dummy_password",
        DB_NAME="dummy_db_name"
    )


@pytest.fixture(scope="session")
def test_app():
    _app = create_app()
    _app.dependency_overrides[get_db] = local_get_db
    _app.dependency_overrides[get_settings] = local_get_settings

    models = [
        Post,
        Word,
        PostWord
    ]
    create_tables(base=Base, engine=_engine, models=models)
    return _app


@pytest.fixture(scope="module")
def test_client(test_app: FastAPI) -> TestClient:
    return TestClient(test_app)
