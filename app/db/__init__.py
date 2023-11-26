from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.configs import settings

engine = create_engine(
    settings.DB_URL, echo=True
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
