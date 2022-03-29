import logging
from typing import Dict, List, Optional
from injector import inject

from paytungan.app.common.utils import ObjectMapperUtil

from .models import Bill, SplitBill
from .interfaces import IBillAccessor, ISplitBillAccessor
from .specs import (
    BillDomain,
    CreateBillSpec,
    CreateSplitBillSpec,
    GetBillListSpec,
    GetBillListResult,
    GetSplitBillListSpec,
)
from paytungan.app.base.constants import DEFAULT_LOGGER


class BillAccessor(IBillAccessor):
    @inject
    def __init__(self) -> None:
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def create(self, obj: BillDomain) -> Bill:
        bill = self._convert_to_model(obj)
        bill.save()
        return bill

    def bulk_create(self, objs: List[BillDomain]) -> List[Bill]:
        objects = self._convert_to_model_list(objects=objs, is_create=True)
        return Bill.objects.bulk_create(objects)

    def get(self, bill_id: int) -> Optional[Bill]:
        try:
            bill = Bill.objects.get(pk=bill_id)
        except Bill.DoesNotExist:
            return None

        return bill

    def get_list(self, spec: GetBillListSpec) -> List[Bill]:
        queryset = Bill.objects

        if spec.bill_ids:
            queryset = queryset.filter(id__in=spec.bill_ids)

        if spec.split_bill_ids:
            queryset = queryset.filter(split_bill__id__in=spec.split_bill_ids)

        if spec.user_ids:
            queryset = queryset.filter(user__id__in=spec.user_ids)

        return queryset

    @staticmethod
    def _convert_to_model(obj: BillDomain, is_create: bool) -> Bill:
        return Bill(
            id=None if is_create else obj.id,
            user_id=obj.user_id,
            split_bill_id=obj.split_bill_id,
            details=obj.details,
            **ObjectMapperUtil.default_model_creation_params()
        )

    def _convert_to_model_list(
        self, objects: List[BillDomain], is_create: bool
    ) -> List[Bill]:
        return [self._convert_to_model(obj, is_create) for obj in objects]


class SplitBillAccessor(ISplitBillAccessor):
    @inject
    def __init__(self) -> None:
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def get(self, id: int) -> Optional[SplitBill]:
        try:
            split_bill = SplitBill.objects.get(pk=id)
        except SplitBill.DoesNotExist:
            return None

        return split_bill

    def get_list(self, spec: GetSplitBillListSpec) -> List[SplitBill]:
        queryset = Bill.objects

        if spec.split_bill_ids:
            queryset = queryset.filter(id__in=spec.split_bill_ids)

        if spec.bill_ids:
            queryset = queryset.filter(bills__id__in=spec.bill_ids)

        if spec.user_fund_ids:
            queryset = queryset.filter(user_fund__id__in=spec.user_fund_ids)

        return queryset

    def create(self, spec: CreateSplitBillSpec) -> SplitBill:
        split_bill = SplitBill(
            name=spec.name,
            user_fund_id=spec.user_fund_id,
            withdrawal_method=spec.withdrawal_method,
            withdrawal_number=spec.withdrawal_number,
            details=spec.details,
            **ObjectMapperUtil.default_model_creation_params()
        )
        split_bill.save()
        return split_bill
