from typing import Set

from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import relationship, Mapped

from app.db.models import Base


class Word(Base):
    __tablename__ = "word"

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    name: str = Column(String(255), nullable=False, index=True)

    posts: Mapped[Set["Post"]] = relationship(
        secondary=None, back_populates='words'
    )
