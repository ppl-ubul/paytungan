from typing import List, Optional
from injector import inject

from paytungan.app.auth.specs import UserDomain
from paytungan.app.base.constants import BillStatus
from paytungan.app.common.exceptions import NotFoundException, ValidationErrorException
from paytungan.app.common.utils import ObjectMapperUtil
from paytungan.app.payment.interfaces import IPaymentAccessor, IXenditProvider
from paytungan.app.payment.models import Payment
from paytungan.app.payment.specs import (
    CreatePaymentSpec,
    CreateXenditInvoiceSpec,
    GetPaymentListSpec,
    PaymentDomain,
    UpdatePaymentSpec,
    UpdateStatusSpec,
    PaymentWithBillDomain,
)
from paytungan.app.split_bill.specs import (
    UpdateBillSpec,
)
from paytungan.app.split_bill.interfaces import IBillAccessor
from datetime import datetime


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
        self, spec: CreatePaymentSpec, user: UserDomain
    ) -> PaymentDomain:
        bill = self.bill_accessor.get(spec.bill_id)

        if not bill:
            raise NotFoundException(f"Bill object with id: {spec.bill_id} not found")

        if bill.user_id != user.id:
            raise ValidationErrorException(
                "User of Bill and user from token don't match"
            )

        if bill.status == BillStatus.PAID.value:
            raise ValidationErrorException("Bill already been paid")

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
                success_redirect_url=spec.success_redirect_url,
                failure_redirect_url=spec.failure_redirect_url,
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

    def update_status(self, spec: UpdateStatusSpec) -> Optional[PaymentWithBillDomain]:
        payment_spec = GetPaymentListSpec(
            bill_ids=list([spec.bill_id]),
        )
        payment = self.payment_accessor.get_list(payment_spec)

        obj_payment = payment[0]
        obj_payment.status = "PAID"
        obj_payment.updated_at = datetime.now()

        update_payment_spec = UpdatePaymentSpec(
            obj=obj_payment, updated_fields=["status", "updated_at"]
        )
        payment = self.payment_accessor.update(update_payment_spec)

        obj_bill = obj_payment.bill
        obj_bill.status = "PAID"
        obj_bill.updated_at = datetime.now()

        update_bill_spec = UpdateBillSpec(
            obj=obj_bill, updated_fields=["status", "updated_at"]
        )
        bill = self.bill_accessor.update(update_bill_spec)

        return PaymentWithBillDomain(
            payment=payment,
            bill=bill,
        )
