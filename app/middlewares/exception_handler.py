from fastapi import Request
from starlette import status
from starlette.responses import JSONResponse

from app.exception import BadRequestException, NotFoundException


async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message, "error_code": exc.error_code}
    )


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message, "error_code": exc.error_code}
    )
