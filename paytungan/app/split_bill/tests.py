# from django.test import TestCase
from unittest import TestCase
from unittest.mock import MagicMock

from paytungan.app.auth.models import User
from paytungan.app.split_bill.services import BillService, SplitBillService
from paytungan.app.split_bill.specs import (
    CreateBillSpec,
    GetBillListSpec,
    GetSplitBillListSpec,
)


class TestService(TestCase):
    def setUp(self) -> None:
        self.mock = MagicMock()
        self.bill_service = BillService(bill_accessor=self.mock)
        self.split_bill_service = SplitBillService(
            split_bill_accessor=self.mock, bill_accessor=self.mock
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
