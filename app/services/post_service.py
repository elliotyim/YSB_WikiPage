from fastapi import Depends

from app.configs import get_settings, Settings
from app.crud.post import PostCrud
from app.crud.word import WordCrud
from app.db import Session, get_db
from app.db.models.post import Post
from app.db.models.word import Word
from app.dto.post import request, response
from app.utils.word_processor import WordProcessor


class PostService:
    def __init__(
            self,
            db: Session = Depends(get_db),
            post_crud: PostCrud = Depends(),
            word_crud: WordCrud = Depends(),
            word_processor: WordProcessor = Depends(),
            settings: Settings = Depends(get_settings)
    ):
        self.db = db
        self.post_crud = post_crud
        self.word_crud = word_crud
        self.word_processor = word_processor
        self._settings = settings

    def get_posts(self, parameter: request.PostList) -> list[response.Post]:
        posts = self.post_crud.find_posts(page=parameter.page, per_page=parameter.per_page)

        return [
            response.Post(
                post_id=post.id,
                post_title=post.title,
                created_date=post.created_at
            ) for post in posts
        ]

    def get_post(self, post_id: int) -> response.PostDetail:
        post = self.post_crud.find_post_with_post_words_by_post_id(post_id=post_id)
        related_word_ids = [post_word.word_id for post_word in post.post_words]

        related_posts = self.post_crud.find_related_posts(
            base_post_id=post.id,
            word_ids=related_word_ids,
            n=self._settings.RELATED_POSTS_AT_ONCE
        )

        return response.PostDetail(
            post_id=post.id,
            post_title=post.title,
            post_content=post.content,
            created_date=post.created_at,
            related_posts=related_posts
        )

    def create_post(self, request_body: request.PostCreate) -> response.PostCreate:
        post = Post(title=request_body.title, content=request_body.content)

        filtered_word_count = self.word_processor.count_related_words(
            content=request_body.content,
            redundant_rate=self._settings.REDUNDANT_RATE
        )
        filtered_words = list(filtered_word_count.keys())

        existing_words = self.word_crud.find_words_by_word_name(word_names=filtered_words)
        new_words = set(filtered_words) - set([word.name for word in existing_words])

        word_count = {word: filtered_word_count[word.name] for word in existing_words}
        for new_word in new_words:
            word_count[Word(name=new_word)] = filtered_word_count[new_word]

        post_words = self.post_crud.save_post_words(post=post, word_count=word_count)
        self.db.commit()

        return response.PostCreate(
            post_id=post.id,
            post_title=post.title,
            post_content=post.content,
            words=[response.Word(word_id=pw.word_id, word=pw.word.name) for pw in post_words]
        )
