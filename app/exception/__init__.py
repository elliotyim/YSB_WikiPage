class BaseRequestException(Exception):
    def __init__(self, message: str, error_code: int):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class BadRequestException(BaseRequestException):
    pass


class NotFoundException(BaseRequestException):
    pass
