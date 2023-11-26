from datetime import datetime
from typing import Set

from sqlalchemy import Text, Column, DateTime, String, BigInteger, func
from sqlalchemy.orm import relationship, Mapped

from app.db.models import Base
from app.db.models.word import Word


class Post(Base):
    __tablename__ = "post"

    id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    title: str = Column(String(255), nullable=False)
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: datetime = Column(DateTime, server_default=func.now(), nullable=False)

    words: Mapped[Set["Word"]] = relationship(
        secondary=None, back_populates='posts'
    )
