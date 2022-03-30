from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction

from paytungan.app.common.decorators import api_exception
from paytungan.app.base.headers import AUTH_HEADERS
from paytungan.app.auth.utils import user_auth
from paytungan.app.auth.specs import UserDecoded
from .specs import (
    CreateBillSpec,
    CreateGroupSplitBillSpec,
    CreateSplitBillSpec,
)
from .serializers import (
    CreateBillRequest,
    CreateBillResponse,
    CreateSplitBillRequest,
    CreateSplitBillResponse,
    GetBillResponse,
    GetBillRequest,
    GetSplitBillResponse,
    GetSplitBillRequest,
    GetListSplitBillRequest,
    GetListSplitBillResponse,
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
        responses={200: GetBillResponse()},
    )
    @api_exception
    def get_bill(self, request: Request) -> Response:
        """
        Get single bill object by id
        """
        serializer = GetBillRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        bill = bill_service.get_bill(data["id"])
        return Response(GetBillResponse({"data": bill}).data)

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
    @transaction.atomic
    @api_exception
    @user_auth
    def create_bill(self, request: Request, user: UserDecoded) -> Response:
        serializer = CreateBillRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        spec = CreateBillSpec(
            user_id=user.id,
            split_bill_id=data["split_bill_id"],
            details=data["details"],
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
        responses={200: GetSplitBillResponse()},
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

    @action(
        detail=False,
        url_path="create",
        methods=["post"],
    )
    @swagger_auto_schema(
        manual_parameters=AUTH_HEADERS,
        request_body=CreateSplitBillRequest(),
        responses={200: CreateSplitBillResponse()},
    )
    @transaction.atomic
    @api_exception
    @user_auth
    def create_split_bill(self, request: Request, user: UserDecoded) -> Response:
        serializer = CreateSplitBillRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        spec = CreateGroupSplitBillSpec(
            name=data["name"],
            user_fund_id=data["user_fund_id"],
            withdrawal_method=data["withdrawal_method"],
            withdrawal_number=data["withdrawal_number"],
            details=data["details"],
            user_ids=data["user_ids"],
        )
        split_bill = split_bill_service.create_group_split_bill(spec)
        return Response(CreateSplitBillResponse({"data": split_bill}).data)

    @action(
        detail=False,
        url_path="get_list",
        methods=["get"],
    )
    @swagger_auto_schema(
        manual_parameters=AUTH_HEADERS,
        responses={200: GetListSplitBillResponse()},
    )
    @api_exception
    @user_auth
    def get_list_split_bill(self, request: Request, user: UserDecoded) -> Response:
        """
        Get list split_bill object
        """
        list_split_bill = split_bill_service.get_split_bill_list(user.id)
        return Response(GetListSplitBillResponse({"data": list_split_bill}).data)
