from datetime import datetime
from typing import Set

from sqlalchemy import Text, Column, DateTime, String, BigInteger, func
from sqlalchemy.orm import relationship, Mapped

from app.db.models import Base
from app.db.models.post_word import PostWord


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = Column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = Column(String(255), nullable=False)
    content: Mapped[str] = Column(Text, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), nullable=False)

    post_words: Mapped[Set[PostWord]] = relationship(back_populates='post')
