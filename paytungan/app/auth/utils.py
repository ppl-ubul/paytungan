from functools import wraps
from urllib import request
from paytungan.app.base.serializers import AuthHeaderRequest


from paytungan.app.di import injector
from paytungan.app.auth.services import AuthService

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
