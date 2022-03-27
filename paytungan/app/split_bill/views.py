from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from paytungan.app.common.decorators import api_exception
from paytungan.app.base.headers import AUTH_HEADERS
from paytungan.app.auth.utils import user_auth
from paytungan.app.auth.specs import UserDecoded
from paytungan.app.split_bill.specs import CreateBillSpec
from .serializers import (
    CreateBillRequest,
    CreateBillResponse,
    GetBillResponse,
    GetBillRequest,
    GetSplitBillResponse,
    GetSplitBillRequest,
)
from .services import (
    BillService,
    SplitBillService,
)
from paytungan.app.di import injector

bill_service = injector.get(BillService)
split_bill_service = injector.get(SplitBillService)


class BillViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        url_path="get",
        methods=["get"],
    )
    @swagger_auto_schema(
        query_serializer=GetBillRequest(),
        responses={200: GetSplitBillResponse()},
    )
    @api_exception
    def get_bill(self, request: Request) -> Response:
        """
        Get single bill object by id
        """
        serializer = GetBillRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = bill_service.get_bill(data["id"])
        return Response(GetSplitBillResponse({"data": user}).data)

    @action(
        detail=False,
        url_path="create",
        methods=["post"],
    )
    @swagger_auto_schema(
        manual_parameters=AUTH_HEADERS,
        request_body=CreateBillRequest(),
        responses={200: CreateBillResponse()},
    )
    @api_exception
    @user_auth
    def create_bill(self, request: Request, user: UserDecoded) -> Response:
        serializer = CreateBillRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        spec = CreateBillSpec(
            user_id=user.id,
            split_bill_id=data["split_bill_id"],
            details=data["details"]
        )
        user = bill_service.create_bill(spec)
        return Response(CreateBillResponse({"data": user}).data)


class SplitBillViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        url_path="get",
        methods=["get"],
    )
    @swagger_auto_schema(
        query_serializer=GetSplitBillRequest(),
        responses={200: GetBillResponse()},
    )
    @api_exception
    def get_split_bill(self, request: Request) -> Response:
        """
        Get single split_bill object by id
        """
        serializer = GetSplitBillRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        split_bill = split_bill_service.get_split_bill(data["id"])
        return Response(GetSplitBillResponse({"data": split_bill}).data)
