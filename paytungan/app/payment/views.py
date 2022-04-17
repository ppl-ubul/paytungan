from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction

from paytungan.app.common.decorators import api_exception
from paytungan.app.base.headers import AUTH_HEADERS
from paytungan.app.auth.utils import firebase_auth, user_auth
from paytungan.app.auth.specs import FirebaseDecodedToken, UserDecoded
from paytungan.app.common.utils import ObjectMapperUtil
from .specs import (
    CreatePaymentSpec,
)
from .serializers import (
    CreatePaymentRequest,
    CreatePaymentResponse,
    GetPaymentResponse,
    GetPaymentRequest,
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
    def get_bill(self, request: Request) -> Response:
        """
        Get single bill object by id
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
    def create_bill(self, request: Request, user: UserDecoded) -> Response:
        serializer = CreatePaymentRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        spec = CreatePaymentSpec(
            bill_id=data["bill_id"],
            method=data["method"],
            reference_no=data["reference_no"],
            status=data["status"],
        )
        user = payment_service.create_bill(spec)
        return Response(CreatePaymentResponse({"data": user}).data)
