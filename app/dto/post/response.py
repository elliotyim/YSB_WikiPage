from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Word(BaseModel):
    word_id: int
    word: Optional[str]


class PostCreate(BaseModel):
    post_id: int
    post_title: Optional[str]
    post_content: Optional[str]
    words: list[Word] = []


class Post(BaseModel):
    post_id: int
    post_title: Optional[str]
    created_date: Optional[datetime]


class PostDetail(BaseModel):
    post_id: int
    post_title: Optional[str]
    post_content: Optional[str]
    created_date: Optional[datetime]
    related_posts: list[Post] = []
