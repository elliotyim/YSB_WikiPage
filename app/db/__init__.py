from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs import get_settings

_settings = get_settings()

engine = create_engine(_settings.DB_URL, echo=True if _settings.ENV != 'prod' else False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()
