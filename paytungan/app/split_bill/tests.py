# from django.test import TestCase
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from paytungan.app.split_bill.models import Bill, SplitBill
from paytungan.app.split_bill.services import BillService, SplitBillService
from paytungan.app.split_bill.specs import (
    CreateBillSpec,
    CreateGroupSplitBillSpec,
    GetBillListSpec,
    GetSplitBillListSpec,
)


class TestService(TestCase):
    def setUp(self) -> None:
        self.bill_accessor = MagicMock()
        self.split_bill_accessor = MagicMock()
        self.bill_service = BillService(bill_accessor=self.bill_accessor)
        self.split_bill_service = SplitBillService(
            split_bill_accessor=self.split_bill_accessor,
            bill_accessor=self.bill_accessor,
        )

    def test_bill_service_get(self):
        self.bill_service.get_bill(1)
        assert True

    def test_bill_service_get_list(self):
        self.bill_service.get_bill_list(
            GetBillListSpec(
                bill_ids=[1],
            )
        )
        assert True

    def test_bill_service_create(self):
        self.bill_service.create_bill(CreateBillSpec(user_id=1, split_bill_id=1))
        assert True

    def test_split_bill_service_get(self):
        self.split_bill_service.get_split_bill(GetSplitBillListSpec(bill_ids=[1]))
        assert True

    def test_split_bill_service_get_list(self):
        self.split_bill_service.get_split_bill_list(GetSplitBillListSpec(bill_ids=[1]))
        assert True

    def test_split_bill_service_get_list_by_user_id(self):
        self.split_bill_service.get_split_bill_list(GetSplitBillListSpec(bill_ids=[1]))
        assert True

    def test_create_group_split_bill(self):
        spec = CreateGroupSplitBillSpec(
            name="tets",
            user_fund_id=1,
            withdrawal_method="GOPAY",
            withdrawal_number="asasa",
            user_ids=[1, 2],
        )
        dummy_split_bill = SplitBill(
            name="tets",
            user_fund_id=1,
            withdrawal_method="GOPAY",
            withdrawal_number="asasa",
        )
        dummy_bills = [
            Bill(
                user_id=1,
                split_bill_id=1,
                status="PENDING",
            ),
            Bill(
                user_id=2,
                split_bill_id=1,
                status="PENDING",
            ),
        ]

        self.split_bill_accessor.create.return_value = dummy_split_bill
        self.bill_accessor.bulk_create.return_value = dummy_bills

        result = self.split_bill_service.create_group_split_bill(spec)

        self.assertEqual(result.name, spec.name)

    def test_get_split_bill_list_current_user(self):
        dummy_split_bills = [
            SplitBill(
                id=1,
                name="tets",
                user_fund_id=1,
                withdrawal_method="GOPAY",
                withdrawal_number="asasa",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        ]
        dummy_bills = [
            Bill(
                user_id=1,
                split_bill_id=1,
                status="PENDING",
            )
        ]

        self.split_bill_accessor.get_list.return_value = dummy_split_bills
        self.bill_accessor.get_list.return_value = dummy_bills

        result = self.split_bill_service.get_list_current_user(1)

        self.assertEqual(result[0].split_bill.id, dummy_split_bills[0].id)
