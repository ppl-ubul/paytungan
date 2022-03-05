from unittest.mock import DEFAULT
from drf_yasg import openapi

token_header = openapi.Parameter(
    "Authentication",
    openapi.IN_HEADER,
    description="Authentication",
    type=openapi.TYPE_STRING,
    required=True,
)

x_request_id = openapi.Parameter(
    "x-request-id",
    openapi.IN_HEADER,
    description="X-Request-Id",
    type=openapi.TYPE_STRING,
)

DEFAULT_HEADERS = [x_request_id]
AUTH_HEADERS = DEFAULT_HEADERS + [token_header]
