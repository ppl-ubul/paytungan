from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock
from xendit import Invoice

from paytungan.app.payment.services import PaymentService
from paytungan.app.payment.specs import (
    CreatePaymentSpec,
    GetPaymentListSpec,
    InvoiceDomain,
    PaymentDomain,
)


class TestService(TestCase):
    def setUp(self) -> None:
        self.payment_accessor = MagicMock()
        self.xendit_provider = MagicMock()
        self.bill_accessor = MagicMock()
        self.payment_service = PaymentService(
            payment_accessor=self.payment_accessor,
            xendit_provider=self.xendit_provider,
            bill_accessor=self.bill_accessor,
        )

    @staticmethod
    def _get_payment_dummy():
        time_now = datetime.now()
        return PaymentDomain(
            id=1,
            updated_at=time_now,
            created_at=time_now,
            bill_id=1,
        )

    @staticmethod
    def _get_invoice_dummy():
        time_now = datetime.now()
        return InvoiceDomain(
            description="fake desc",
            invoice_url="fake_url",
            expiry_date=time_now,
            status="PENDING",
            amount=20000,
        )

    def test_get_payment_success(self) -> None:
        fake_payment = self._get_payment_dummy()
        fake_invoice = self._get_invoice_dummy()

        self.payment_accessor.get.return_value = fake_payment
        self.xendit_provider.get_invoice.return_value = fake_invoice
        payment = self.payment_service.get_payment(fake_payment.id)

        self.assertEqual(payment.invoice, fake_invoice)

    def test_get_payment_empty(self) -> None:
        self.payment_accessor.get.return_value = None
        payment = self.payment_service.get_payment(1)

        self.assertEqual(payment, None)

    def test_get_list_payment(self) -> None:
        spec = GetPaymentListSpec(
            user_id=1,
        )

        self.payment_service.get_payment_list(spec)

        self.assertTrue(1)
