from enum import IntEnum


class ErrorCode(IntEnum):
    WRONG_PAGE_NUMBER_PROVIDED = 1000
    WRONG_PER_PAGE_NUMBER_PROVIDED = 1001

    NO_SUCH_POST_EXIST = 2000
