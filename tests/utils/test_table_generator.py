import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base
from app.db.models.post import Post
from app.db.models.post_word import PostWord
from app.db.models.word import Word
from app.utils.table_generator import create_tables


class TestTableGenerator:
    def test_creating_tables(self):
        engine = create_engine('sqlite://')
        SessionLocal = sessionmaker(bind=engine)

        with pytest.raises(Exception):
            with SessionLocal() as db:
                db.query(Post).all()

        models = [Post, Word, PostWord]
        create_tables(base=Base, engine=engine, models=models)

        with SessionLocal() as db:
            posts = db.query(Post).all()
            post_words = db.query(PostWord).all()
            words = db.query(Word).all()

            assert len(posts) == 0
            assert len(post_words) == 0
            assert len(words) == 0
