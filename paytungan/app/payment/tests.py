from unittest import TestCase
from unittest.mock import MagicMock

from paytungan.app.payment.services import PaymentService
from paytungan.app.payment.specs import CreatePaymentSpec, GetPaymentListSpec


class TestService(TestCase):
    def setUp(self) -> None:
        self.payment_accessor = MagicMock()
        self.payment_service = PaymentService(payment_accessor=self.payment_accessor)

    def test_get_payment(self) -> None:
        self.payment_service.get_payment(1)

        self.assertTrue(1)

    def test_get_list_payment(self) -> None:
        spec = GetPaymentListSpec(
            user_id=1,
        )

        self.payment_service.get_payment_list(spec)

        self.assertTrue(1)

    def test_create_payment(self) -> None:
        spec = CreatePaymentSpec(
            bill_id=1,
            method="GOPAY",
            reference_no="asas1",
            status="PENDING",
        )

        self.payment_service.create_payment(spec)
        self.assertTrue(1)
