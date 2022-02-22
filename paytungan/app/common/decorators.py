from functools import wraps
import jwt


def jwt_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Decorator
        """
        func(*args, **kwargs)

    return wrapper
