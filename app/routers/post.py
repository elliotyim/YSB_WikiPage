from fastapi import APIRouter, Depends

from app.dto.post import response, request
from app.services.post_service import PostService

router = APIRouter()


@router.get("")
def get_posts(
        query_parameter: request.PostList = Depends(),
        post_service: PostService = Depends()
) -> list[response.Post]:
    posts = post_service.get_posts(parameter=query_parameter)
    return posts


@router.post("")
def create_post(
        request_body: request.PostCreate,
        post_service: PostService = Depends()
) -> response.PostCreate:
    created_post = post_service.create_post(request_body=request_body)
    return created_post
