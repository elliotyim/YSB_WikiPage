from fastapi import Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db import get_db
from app.db.models.word import Word
from app.utils.word_processor import WordProcessor


class WordCrud:
    def __init__(self, db: Session = Depends(get_db), word_processor: WordProcessor = Depends()):
        self.db = db
        self.word_processor = word_processor

    def find_words_by_word_name(self, word_names: list[str]) -> list[Word]:
        existing_words = self.db.query(Word).filter(
            or_(
                (Word.name == word_name for word_name in word_names)
            )
        ).all()
        return existing_words

