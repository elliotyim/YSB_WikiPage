from typing import Set

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship, Mapped

from app.db.models import Base
from app.db.models.post_word import PostWord


class Word(Base):
    __tablename__ = "word"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String(255), nullable=False, unique=True, index=True)

    post_words: Mapped[Set[PostWord]] = relationship(back_populates='word')
