from functools import cache
from typing import Generator

from fastapi import Depends
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from app.configs import get_settings


@cache
def get_engine() -> Engine:
    _settings = get_settings()
    return create_engine(_settings.DB_URL, echo=True if _settings.ENV != 'prod' else False)


@cache
def get_session_maker(engine: Engine = Depends(get_engine)):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(session_local: sessionmaker = Depends(get_session_maker)) -> Generator[Session, None, None]:
    with session_local() as db:
        yield db
    a = 2
