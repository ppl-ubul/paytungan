from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .interfaces import IUserServices

from .serializers import GetUserRequest, GetUserResponse
from paytungan.app.di import injector

user_service = injector.get(IUserServices)


class UserViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        url_path="get",
        methods=["get"],
    )
    @swagger_auto_schema(
        # manual_parameters=ENDPOINT_DEFAULT_PARAMS,
        query_serializer=GetUserRequest(),
        responses={200: GetUserResponse()},
    )
    def get_user(self, request: Request) -> Response:
        """
        Get single principal object
        by principal id or principal name
        """
        # header_serializer = BaseHeaderRequestSerializer(data=request.headers)
        # header_serializer.is_valid(raise_exception=True)
        serializer = GetUserRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = user_service.get(data["user_id"])
        return Response(GetUserResponse({"data": user}).data)
