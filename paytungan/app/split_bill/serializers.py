from rest_framework import serializers


class GetBillRequest(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)


class BillSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)
    split_bill_id = serializers.IntegerField(min_value=1)
    details = serializers.CharField(required=False, allow_null=True)


class GetBillResponse(serializers.Serializer):
    data = BillSerializer()


class CreateBillRequest(serializers.Serializer):
    split_bill_id = serializers.IntegerField(min_value=1)
    details = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class CreateBillResponse(serializers.Serializer):
    data = BillSerializer()


class GetSplitBillRequest(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)


class SplitBillSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField()
    user_fund_id = serializers.IntegerField(min_value=1)
    withdrawal_method = serializers.CharField(required=False)
    withdrawal_number = serializers.CharField(required=False)
    details = serializers.CharField(required=False, allow_null=True)


class GetSplitBillResponse(serializers.Serializer):
    data = SplitBillSerializer()
