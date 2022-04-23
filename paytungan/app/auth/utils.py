from functools import wraps

from paytungan.app.auth.specs import UserDomain
from paytungan.app.base.serializers import AuthHeaderRequest
from paytungan.app.common.exceptions import UnauthorizedError
from paytungan.app.common.utils import ObjectMapperUtil
from paytungan.app.auth.services import AuthService
from paytungan.app.di import injector

auth_service: AuthService = injector.get(AuthService)


def firebase_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator for views method to get auth request
        """
        request = args[1]
        header_serializer = AuthHeaderRequest(data=request.headers)
        header_serializer.is_valid(raise_exception=True)
        token = header_serializer.data["Authentication"]
        user = auth_service.decode_token(token)
        return func(*args, user, **kwargs)

    return wrapper


def user_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator for views method to get auth request
        """
        request = args[1]
        header_serializer = AuthHeaderRequest(data=request.headers)
        header_serializer.is_valid(raise_exception=True)
        token = header_serializer.data["Authentication"]
        user = auth_service.get_user_from_token(token)
        cred = ObjectMapperUtil.map(user, UserDomain)
        if not user:
            raise UnauthorizedError(
                message="User with current token is not found", code=403
            )

        return func(*args, cred, **kwargs)

    return wrapper
