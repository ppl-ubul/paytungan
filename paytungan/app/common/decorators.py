from functools import wraps
from rest_framework.exceptions import ValidationError

from paytungan.app.common.exceptions import (
    NotFoundException,
    ValidationErrorException,
    OurValidationError
)


def jwt_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator
        """
        func(*args, **kwargs)

    return wrapper


def api_exception(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        """
        Catch any exception that happens in API function then convert it into DRF exception

        Background:
            There are validations that need to be done in core domain. When specs do not meet
            the function requirement, the function should raise a validation error.
            Since core domain need to be independent from any dependencies, we create our custom
            exception for our core domain.
        """

        try:
            return function(*args, **kwargs)
        except OurValidationError as error:
            raise error
        except ValidationErrorException as error:
            raise OurValidationError(message=error.message, detail=error.field_errors)
        except NotFoundException as error:
            raise OurValidationError(message=error.message, detail={})
        except ValidationError as error:
            raise OurValidationError(detail=error.detail)
        except Exception as error:
            raise error

    return wrapper
