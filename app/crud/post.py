from fastapi import Depends
from sqlalchemy import or_, func, desc, select
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.db.models.post import Post
from app.db.models.post_word import PostWord
from app.db.models.word import Word
from app.dto.post import response
from app.utils.word_processor import WordProcessor


class PostCrud:

    def __init__(self, db: Session = Depends(get_db), word_processor: WordProcessor = Depends()):
        self.db = db
        self.word_processor = word_processor

    def find_posts(self, page: int, per_page: int) -> list[Post]:
        posts = self.db.query(Post).limit(per_page).offset((page - 1) * per_page).all()
        return posts

    def find_post_with_post_words_by_post_id(self, post_id: int) -> Post:
        post = self.db.query(Post).options(joinedload(Post.post_words)).filter(Post.id == post_id).one()
        return post

    def find_related_posts(self, base_post_id: int, word_ids: list[int], n: int) -> list[response.Post]:
        # Word relation score
        subquery = (
            select(
                PostWord.post_id.label("post_id0"),
                PostWord.word_id.label("word_id0"),
                func.sum(PostWord.count).label("score")
            )
            .select_from(PostWord)
            .group_by(PostWord.post_id, PostWord.word_id)
            .subquery()
        )

        related_posts = (
            self.db.query(
                PostWord.post_id,
                Post.title,
                Post.created_at,
                func.sum(subquery.c.score)
            )
            .select_from(PostWord)
            .join(Post)
            .join(
                subquery,
                (PostWord.post_id == subquery.c.post_id0) & (PostWord.word_id == subquery.c.word_id0)
            )
            .filter(PostWord.post_id != base_post_id)
            .filter(or_((PostWord.word_id == word_id for word_id in word_ids)))
            .group_by(PostWord.post_id, Post.title, Post.created_at)
            .having(func.count(PostWord.post_id) >= 2)
            .order_by(desc(func.sum(subquery.c.score)), PostWord.post_id)
            .limit(n)
            .all()
        )

        return [
            response.Post(
                post_id=post_id,
                post_title=post_title,
                created_date=created_date
            ) for post_id, post_title, created_date, count in related_posts
        ]

    def save_post_words(self, post: Post, word_count: dict[Word, int]) -> list[PostWord]:
        post_words = [
            PostWord(
                count=count,
                post=post,
                word=word
            ) for word, count in word_count.items()
        ]
        self.db.add_all(post_words)
        return post_words
