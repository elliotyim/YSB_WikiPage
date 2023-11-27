from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from app.db.models import Base


class PostWord(Base):
    __tablename__ = "post_word"

    post_id: Mapped[int] = Column(ForeignKey('post.id'), primary_key=True)
    word_id: Mapped[int] = Column(ForeignKey('word.id'), primary_key=True)
    post: Mapped["Post"] = relationship(back_populates="post_words")
    word: Mapped["Word"] = relationship(back_populates="post_words")
