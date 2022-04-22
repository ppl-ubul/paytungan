from rest_framework import serializers

from paytungan.app.common.utils import EnumUtil


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