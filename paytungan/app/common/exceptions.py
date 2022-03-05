import json
from typing import Optional, Dict, List
from rest_framework.exceptions import ValidationError


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


class UnauthorizedError(BaseException):
    def __init__(
        self, message: str = "Unauthorized Request.", code: Optional[str] = None
    ):
        super().__init__(message=message, code=code)


class OurValidationError(ValidationError):
    """
    Override default DRF ValidationError to enable raising validation
    error (with error of each field) from outside serializer.
    """

    def __init__(
        self,
        message: str = "Something went wrong.",
        detail: Optional[Dict[str, List[str]]] = None,
        code: Optional[str] = None,
    ):
        super().__init__(detail=detail, code=code)
        self.message = message
        self.code = code

    @property
    def details(self):
        """
        Default DRF ValidationError uses self.detail to store detail of its fields' errors.
        Since we could not override the self.detail value and its default value type is
        OrderedDict, we have to create new @property to convert it to json first.
        """
        data = self.detail
        return json.loads(json.dumps(data))
