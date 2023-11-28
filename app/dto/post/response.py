from typing import Optional

from pydantic import BaseModel


class Word(BaseModel):
    word_id: Optional[int]
    word: Optional[str]


class PostCreate(BaseModel):
    post_id: Optional[int]
    post_title: Optional[str]
    post_content: Optional[str]
    words: list[Word] = []
