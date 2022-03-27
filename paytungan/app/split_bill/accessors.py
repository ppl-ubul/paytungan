import logging
from typing import Dict, List, Optional
from injector import inject

from paytungan.app.common.utils import ObjectMapperUtil

from .models import Bill, SplitBill
from .interfaces import IBillAccessor, ISplitBillAccessor
from .specs import (
    CreateBillSpec,
    GetBillListSpec,
    GetBillListResult,
    GetSplitBillListSpec,
)
from paytungan.app.base.constants import DEFAULT_LOGGER


class BillAccessor(IBillAccessor):
    @inject
    def __init__(self) -> None:
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def create(self, spec: CreateBillSpec) -> Bill:
        bill = Bill(
            user_id=spec.user_id,
            split_bill_id=spec.split_bill_id,
            details=spec.details,
            **ObjectMapperUtil.default_model_creation_params()
        )
        bill.save()
        return bill

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
