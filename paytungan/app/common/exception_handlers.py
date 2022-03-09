from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .exceptions import OurValidationError
from .responses import ErrorResponse


def paytungan_exception_handler(exception, context):
    """
    Call REST framework's default exception handler first, to get the standard error response.
    Then add HTTP status code.

    If DRF does not catch the exception, we will wrap it into Response 500.
    """
    response = exception_handler(exception, context)
    details = None
    code = None
    if not response:
        status_code = getattr(
            exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            return None
        response = Response(status=status_code)
        message = str(exception)
    elif _is_custom_exception(exception):
        message = getattr(exception, "message", None)
        details = getattr(exception, "details", None)
        code = getattr(exception, "code", None)
    else:
        error_detail: ErrorDetail = getattr(exception, "detail", None)
        message = str(error_detail) if error_detail else ""
        code = getattr(error_detail, "code", None)

    response.data = ErrorResponse(
        error_message=message, validation_error=details, code=code
    ).error
    return response


def _is_custom_exception(exception) -> bool:
    # Return True if exception is instance of custom DRF exception
    return isinstance(exception, OurValidationError)
