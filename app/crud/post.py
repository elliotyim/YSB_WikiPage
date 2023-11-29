from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models.post import Post
from app.db.models.post_word import PostWord
from app.db.models.word import Word
from app.utils.word_processor import WordProcessor


class PostCrud:

    def __init__(self, db: Session = Depends(get_db), word_processor: WordProcessor = Depends()):
        self.db = db
        self.word_processor = word_processor

    def generate_words(self, words: list[str]) -> list[Word]:
        word_set = set(words)

        existing_words = self.db.query(Word).filter(
            or_(
                (Word.name == word for word in words)
            )
        ).all()

        for word in existing_words:
            word_set.remove(word.name)

        return existing_words + [Word(name=word) for word in word_set]

    def find_posts(self, page: int, per_page: int) -> list[Post]:
        posts = self.db.query(Post).limit(per_page).offset((page - 1) * per_page).all()
        return posts

    def save_post_and_words(self, post: Post, words: list[Word]) -> list[PostWord]:
        post_words = [PostWord(post=post, word=word) for word in words]
        self.db.add_all(post_words)
        return post_words
