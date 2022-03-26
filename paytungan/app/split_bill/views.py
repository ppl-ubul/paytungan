from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from paytungan.app.common.decorators import api_exception
from .serializers import (
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
    def get_split_bill(self, request: Request) -> Response:
        """
        Get single user object by user id
        """
        serializer = GetBillRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = bill_service.get_bill(data["id"])
        return Response(GetSplitBillResponse({"data": user}).data)


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
    def get_bill(self, request: Request) -> Response:
        """
        Authentication Login and Register
        """
        serializer = GetSplitBillRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        split_bill = split_bill_service.get_split_bill(data["id"])
        return Response(GetSplitBillResponse({"data": split_bill}).data)
