from sqlalchemy import Column, ForeignKey

from app.db.models import Base


class PostWord(Base):
    __tablename__ = "post_word"

    post_id: int = Column(ForeignKey('post.id'), primary_key=True)
    word_id: int = Column(ForeignKey('word.id'), primary_key=True)
