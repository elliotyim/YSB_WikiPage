from fastapi import Depends

from app.configs import get_settings, Settings
from app.crud.post import PostCrud
from app.db import Session, get_db
from app.db.models.post import Post
from app.dto.post import request, response
from app.utils.word_processor import WordProcessor


class PostService:
    def __init__(
            self,
            db: Session = Depends(get_db),
            post_crud: PostCrud = Depends(),
            word_processor: WordProcessor = Depends(),
            settings: Settings = Depends(get_settings)
    ):
        self.db = db
        self.post_crud = post_crud
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

    def create_post(self, request_body: request.PostCreate) -> response.PostCreate:
        filtered_words = self.word_processor.count_related_words(
            content=request_body.content,
            redundant_rate=self._settings.REDUNDANT_RATE
        )

        words = self.post_crud.generate_words(words=list(filtered_words.keys()))
        post = Post(title=request_body.title, content=request_body.content)
        post_words = self.post_crud.save_post_and_words(post=post, words=words)

        self.db.commit()

        post_dto = response.PostCreate(
            post_id=post.id,
            post_title=post.title,
            post_content=post.content,
            words=[response.Word(word_id=pw.word_id, word=pw.word.name) for pw in post_words]
        )

        return post_dto
