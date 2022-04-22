from typing import List, Optional
from injector import inject

from paytungan.app.auth.specs import UserDecoded
from paytungan.app.base.constants import BillStatus
from paytungan.app.common.exceptions import NotFoundException, ValidationError
from paytungan.app.common.utils import ObjectMapperUtil
from paytungan.app.payment.interfaces import IPaymentAccessor, IXenditProvider
from paytungan.app.payment.models import Payment
from paytungan.app.payment.specs import (
    CreatePaymentSpec,
    CreateXenditInvoiceSpec,
    GetPaymentListSpec,
    PaymentDomain,
    UpdatePaymentSpec,
)
from paytungan.app.split_bill.interfaces import IBillAccessor


class PaymentService:
    @inject
    def __init__(
        self,
        payment_accessor: IPaymentAccessor,
        xendit_provider: IXenditProvider,
        bill_accessor: IBillAccessor,
    ) -> None:
        self.payment_accessor = payment_accessor
        self.xendit_provider = xendit_provider
        self.bill_accessor = bill_accessor

    def get_payment(self, payment_id: int) -> Optional[PaymentDomain]:
        payment = self.payment_accessor.get(payment_id)

        if not payment:
            return None

        invoice = self.xendit_provider.get_invoice(payment.reference_no)
        payment.invoice = invoice
        payment.payment_url = invoice.invoice_url

        return payment

    def get_payment_list(self, spec: GetPaymentListSpec) -> List[Payment]:
        return self.payment_accessor.get_list(spec)

    def create_payment(
        self, spec: CreatePaymentSpec, user: UserDecoded
    ) -> PaymentDomain:
        bill = self.bill_accessor.get(spec.bill_id)

        if not bill:
            raise NotFoundException(f"Bill object with id: {spec.bill_id} not found")

        if bill.user_id != user.id:
            raise ValidationError("User of Bill and user from token don't match")

        if bill.status == BillStatus.PAID.value:
            raise ValidationError("Bill already been paid")

        payment = self.payment_accessor.create(
            PaymentDomain(
                bill_id=spec.bill_id,
                **ObjectMapperUtil.default_domain_creation_params(),
            )
        )

        invoice = self.xendit_provider.create_invoice(
            CreateXenditInvoiceSpec(
                external_id=str(payment.id),
                amount=payment.amount,
                payer_email=user.email,
                description=payment.number,
            )
        )

        payment.reference_no = invoice.id
        payment.expiry_date = invoice.expiry_date
        payment.invoice = invoice
        payment.payment_url = invoice.invoice_url
        self.payment_accessor.update(
            UpdatePaymentSpec(payment, updated_fields=["reference_no", "expiry_date"])
        )

        return payment
