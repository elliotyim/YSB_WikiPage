import uvicorn
from fastapi import FastAPI

from app.configs import get_settings
from app.routers import post


def create_app() -> FastAPI:
    _app = FastAPI()
    _app.include_router(post.router, prefix='/posts', tags=["posts"])
    return _app


app = create_app()

if __name__ == '__main__':
    settings = get_settings()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
