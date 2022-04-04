from typing import List, Optional
from injector import inject

from paytungan.app.base.constants import BillStatus
from paytungan.app.common.utils import ObjectMapperUtil
from .models import Bill, SplitBill
from .interfaces import (
    IBillAccessor,
    ISplitBillAccessor,
)
from .specs import (
    BillDomain,
    CreateBillSpec,
    CreateGroupSplitBillSpec,
    CreateSplitBillSpec,
    DeleteSplitBillSpec,
    GetBillListSpec,
    GetSplitBillListSpec,
    GroupSplitBillDomain,
    SplitBillWithBillDomain,
)


class BillService:
    @inject
    def __init__(self, bill_accessor: IBillAccessor) -> None:
        self.bill_accessor = bill_accessor

    def get_bill(self, bill_id: int) -> Optional[Bill]:
        return self.bill_accessor.get(bill_id)

    def get_bill_list(self, spec: GetBillListSpec) -> List[Bill]:
        return self.bill_accessor.get(spec)

    def create_bill(self, spec: CreateBillSpec) -> Bill:
        return self.bill_accessor.create(spec)


class SplitBillService:
    @inject
    def __init__(
        self,
        bill_accessor: IBillAccessor,
        split_bill_accessor: ISplitBillAccessor,
    ) -> None:
        self.bill_accessor = bill_accessor
        self.split_bill_accessor = split_bill_accessor

    def get_split_bill(self, split_bill_id: int) -> Optional[SplitBill]:
        return self.split_bill_accessor.get(split_bill_id)

    def get_split_bill_list(self, spec: GetSplitBillListSpec) -> List[SplitBill]:
        return self.split_bill_accessor.get_list(spec)

    def create_split_bill(self, spec: CreateSplitBillSpec) -> SplitBill:
        return self.split_bill_accessor.create(spec)

    def create_group_split_bill(
        self, spec: CreateGroupSplitBillSpec
    ) -> GroupSplitBillDomain:
        split_bill_create_spec = ObjectMapperUtil.map(spec, CreateSplitBillSpec)
        split_bill = self.create_split_bill(split_bill_create_spec)

        bills_domain = [
            BillDomain(
                user_id=user_id,
                split_bill_id=split_bill.id,
                **ObjectMapperUtil.default_domain_creation_params()
            )
            for user_id in spec.user_ids
        ]

        bills_domain.append(
            BillDomain(
                user_id=spec.user_fund_id,
                split_bill_id=split_bill.id,
                status=BillStatus.PAID.value,
                **ObjectMapperUtil.default_domain_creation_params()
            )
        )
        bills = self.bill_accessor.bulk_create(bills_domain)

        return GroupSplitBillDomain(
            id=split_bill.id,
            created_at=split_bill.created_at,
            updated_at=split_bill.updated_at,
            name=split_bill.name,
            user_fund_id=split_bill.user_fund_id,
            withdrawal_method=split_bill.withdrawal_method,
            withdrawal_number=split_bill.withdrawal_number,
            details=split_bill.details,
            bills=bills,
        )

    def get_list_current_user(self, user_id: int) -> List[SplitBillWithBillDomain]:
        bills = self.bill_accessor.get_list(
            GetBillListSpec(
                user_ids=[user_id],
            )
        )

        if not bills:
            return []

        split_bills_ids = [bill.split_bill_id for bill in bills]
        split_bills = self.split_bill_accessor.get_list(
            GetSplitBillListSpec(split_bill_ids=split_bills_ids)
        )

        if not split_bills:
            return []

        split_bill_to_bill_mapping = {bill.split_bill_id: bill for bill in bills}
        return [
            SplitBillWithBillDomain(
                split_bill=split_bill,
                bill=split_bill_to_bill_mapping[split_bill.id],
            )
            for split_bill in split_bills
        ]

    def delete(self, spec: DeleteSplitBillSpec) -> None:
        return self.split_bill_accessor.delete(spec)
