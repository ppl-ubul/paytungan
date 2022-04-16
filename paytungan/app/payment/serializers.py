from rest_framework import serializers

from paytungan.app.common.utils import EnumUtil


class GetPaymentRequest(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)


class PaymentSerializers(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    bill_id = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
    method = serializers.CharField()
    number = serializers.CharField()
    reference_no = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class GetPaymentResponse(serializers.Serializer):
    data = PaymentSerializers()
