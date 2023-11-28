from fastapi.params import Query
from pydantic import BaseModel

from app.exception.error_code import ErrorCode
from app.middlewares.exception_handler import BadRequestException


class PostList:
    def __init__(
            self,
            page: int = Query(default=1, description='<p><b>조회 할 페이지</b><p>'
                                                     '<p>페이지는 1부터 시작</p>'),
            per_page: int = Query(default=10, description='한 페이지 당 보여줄 게시글의 갯수')
    ):
        if page < 1:
            raise BadRequestException(
                message="page must be greater than 0",
                error_code=ErrorCode.WRONG_PAGE_NUMBER_PROVIDED
            )
        elif per_page < 1 or per_page > 100:
            raise BadRequestException(
                message="per_page must be greater than 0 and less than 100",
                error_code=ErrorCode.WRONG_PER_PAGE_NUMBER_PROVIDED
            )

        self.page = page
        self.per_page = per_page


class PostCreate(BaseModel):
    title: str
    content: str
