from typing import Optional, Dict, List


class BaseException(Exception):
    def __init__(
        self, message: str = "Something went wrong.", code: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.code = code


class ValidationErrorException(BaseException):
    def __init__(
        self,
        message: str = "Invalid data.",
        code: Optional[str] = None,
        field_errors: Optional[Dict[str, List[str]]] = None,
    ):
        super().__init__(message=message, code=code)
        self.field_errors = field_errors or {}


class NotFoundException(BaseException):
    def __init__(self, message: str = "Not found.", code: Optional[str] = None):
        super().__init__(message=message, code=code)
