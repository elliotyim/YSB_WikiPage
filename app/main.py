import uvicorn
from fastapi import FastAPI

from app.configs import settings


def create_app() -> FastAPI:
    _app = FastAPI()
    return _app


if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
