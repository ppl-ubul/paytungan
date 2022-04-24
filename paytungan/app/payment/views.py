from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction

from paytungan.app.common.decorators import api_exception
from paytungan.app.base.headers import AUTH_HEADERS
from paytungan.app.auth.utils import user_auth, firebase_auth
from paytungan.app.auth.specs import UserDomain, FirebaseDecodedToken

from .specs import (
    CreatePaymentSpec,
    UpdateStatusSpec,
)
from .serializers import (
    CreatePaymentRequest,
    CreatePaymentResponse,
    GetPaymentResponse,
    GetPaymentRequest,
    UpdateStatusRequest,
    UpdateStatusResponse,
    GetPaymentByBillIdRequest,
    GetPaymentByBillIdResponse,
)
from .services import (
    PaymentService,
)
from paytungan.app.di import injector

payment_service = injector.get(PaymentService)


class PaymentViewSet(viewsets.ViewSet):
    @action(
        detail=False,
        url_path="get",
        methods=["get"],
    )
    @swagger_auto_schema(
        query_serializer=GetPaymentRequest(),
        responses={200: GetPaymentResponse()},
    )
    @api_exception
    def get_payment(self, request: Request) -> Response:
        """
        Get single payment object by id
        """
        serializer = GetPaymentRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        payment = payment_service.get_payment(data["id"])
        return Response(GetPaymentResponse({"data": payment}).data)

    @action(
        detail=False,
        url_path="create",
        methods=["post"],
    )
    @swagger_auto_schema(
        manual_parameters=AUTH_HEADERS,
        request_body=CreatePaymentRequest(),
        responses={200: CreatePaymentResponse()},
    )
    @transaction.atomic
    @api_exception
    @user_auth
    def create_payment(self, request: Request, user: UserDomain) -> Response:
        serializer = CreatePaymentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        spec = CreatePaymentSpec(
            bill_id=data["bill_id"],
            success_redirect_url=data["success_redirect_url"],
            failure_redirect_url=data["failure_redirect_url"],
        )
        user = payment_service.create_payment(spec, user)
        return Response(CreatePaymentResponse({"data": user}).data)

    @action(
        detail=False,
        url_path="update/paid",
        methods=["post"],
    )
    @swagger_auto_schema(
        manual_parameters=AUTH_HEADERS,
        request_body=UpdateStatusRequest(),
        responses={200: UpdateStatusResponse()},
    )
    @transaction.atomic
    @api_exception
    @firebase_auth
    def update_user(self, request: Request, cred: FirebaseDecodedToken) -> Response:
        """
        Update Status
        """
        serializer = UpdateStatusRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        spec = UpdateStatusSpec(
            bill_id=data["bill_id"],
        )
        payment = payment_service.update_status(spec)
        return Response(UpdateStatusResponse({"data": payment}).data)

    @action(
        detail=False,
        url_path="get/bill_id",
        methods=["get"],
    )
    @swagger_auto_schema(
        manual_parameters=AUTH_HEADERS,
        query_serializer=GetPaymentByBillIdRequest(),
        responses={200: GetPaymentByBillIdResponse()},
    )
    @api_exception
    @firebase_auth
    def get_split_bill_list(
        self, request: Request, cred: FirebaseDecodedToken
    ) -> Response:
        """
        Get payment by bill id
        """
        serializer = GetPaymentByBillIdRequest(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        payment = payment_service.get_payment_by_bill_id(data["bill_id"])
        return Response(GetPaymentByBillIdResponse({"data": payment}).data)
