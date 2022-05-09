from rest_framework import serializers

from paytungan.app.common.utils import EnumUtil
from paytungan.app.split_bill.serializers import BillSerializer


class GetPaymentRequest(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)


class XenditInvoiceSerializers(serializers.Serializer):
    description = serializers.CharField()
    invoice_url = serializers.CharField()
    payment_method = serializers.CharField(required=False)
    status = serializers.CharField()
    amount = serializers.IntegerField()
    expiry_date = serializers.DateTimeField()
    paid_amount = serializers.IntegerField(required=False)
    payer_email = serializers.CharField(required=False)
    paid_at = serializers.DateTimeField(required=False)
    success_redirect_url = serializers.CharField(required=False)
    failure_redirect_url = serializers.CharField(required=False)


class XenditPayoutSerializers(serializers.Serializer):
    id = serializers.CharField()
    external_id = serializers.CharField()
    amount = serializers.IntegerField()
    status = serializers.CharField()
    expiration_timestamp = serializers.DateTimeField()
    created = serializers.DateTimeField()
    email = serializers.CharField()
    payout_url = serializers.CharField()


class PaymentSerializers(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    bill_id = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    method = serializers.CharField()
    reference_no = serializers.CharField()
    expiry_date = serializers.DateTimeField()
    paid_at = serializers.DateTimeField()
    number = serializers.CharField()
    amount = serializers.IntegerField()
    payment_url = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    invoice = XenditInvoiceSerializers()


class GetPaymentResponse(serializers.Serializer):
    data = PaymentSerializers()


class CreatePaymentRequest(serializers.Serializer):
    bill_id = serializers.IntegerField(min_value=1)
    success_redirect_url = serializers.CharField(required=False)
    failure_redirect_url = serializers.CharField(required=False)


class CreatePaymentResponse(serializers.Serializer):
    data = PaymentSerializers()


class UpdateStatusRequest(serializers.Serializer):
    bill_id = serializers.IntegerField(min_value=1)


class PaymentWithBillDomain(serializers.Serializer):
    payment = PaymentSerializers()
    bill = BillSerializer()


class UpdateStatusResponse(serializers.Serializer):
    data = PaymentWithBillDomain()


class GetPaymentByBillIdRequest(serializers.Serializer):
    bill_id = serializers.IntegerField(min_value=1)


class GetPaymentByBillIdResponse(serializers.Serializer):
    data = PaymentSerializers()


class GetPayoutRequest(serializers.Serializer):
    split_bill_id = serializers.IntegerField(min_value=1)


class GetPayoutResponse(serializers.Serializer):
    data = XenditPayoutSerializers()


class CreatePayoutRequest(serializers.Serializer):
    split_bill_id = serializers.IntegerField(min_value=1)


class CreatePayoutResponse(serializers.Serializer):
    data = XenditPayoutSerializers()
