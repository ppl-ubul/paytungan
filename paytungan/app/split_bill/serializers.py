from rest_framework import serializers
from paytungan.app.base.constants import WithdrawalMethod

from paytungan.app.common.utils import EnumUtil


class GetBillRequest(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)


class BillSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1)
    user_id = serializers.IntegerField(min_value=1)
    split_bill_id = serializers.IntegerField(min_value=1)
    status = serializers.CharField()
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


class GroupSplitBillSerializer(SplitBillSerializer):
    bills = BillSerializer(many=True)


class GetSplitBillResponse(serializers.Serializer):
    data = SplitBillSerializer()


class CreateSplitBillRequest(serializers.Serializer):
    name = serializers.CharField()
    user_fund_id = serializers.IntegerField(min_value=1)
    withdrawal_method = serializers.ChoiceField(
        choices=EnumUtil.extract_enum_values(WithdrawalMethod)
    )
    withdrawal_number = serializers.CharField()
    details = serializers.CharField(required=False, allow_null=True)
    user_ids = serializers.ListField(child=serializers.IntegerField(min_value=1))


class CreateSplitBillResponse(serializers.Serializer):
    data = GroupSplitBillSerializer()


class SplitBillWithBillCurrentUserSerializer(serializers.Serializer):
    split_bill = SplitBillSerializer()
    bill = BillSerializer()


class GetListSplitBillRequest(serializers.Serializer):
    user_id = serializers.IntegerField(min_value=1)


class GetListSplitBillResponse(serializers.Serializer):
    data = SplitBillWithBillCurrentUserSerializer(many=True)