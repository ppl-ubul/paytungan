from typing import List, Optional
from injector import inject

from paytungan.app.common.utils import ObjectMapperUtil
from paytungan.app.payment.interfaces import IPaymentAccessor
from paytungan.app.payment.models import Payment
from paytungan.app.payment.specs import (
    CreatePaymentSpec,
    GetPaymentListSpec,
    PaymentDomain,
)


class PaymentService:
    @inject
    def __init__(self, payment_accessor: IPaymentAccessor) -> None:
        self.payment_accessor = payment_accessor

    def get_payment(self, payment_id: int) -> Optional[Payment]:
        return self.payment_accessor.get(payment_id)

    def get_payment_list(self, spec: GetPaymentListSpec) -> List[Payment]:
        return self.payment_accessor.get_list(spec)

    def create_payment(self, spec: CreatePaymentSpec) -> Payment:
        payment = PaymentDomain(
            bill_id=spec.bill_id,
            status=spec.status,
            method=spec.method,
            reference_no=spec.reference_no,
            **ObjectMapperUtil.default_domain_creation_params()
        )
        return self.payment_accessor.create(payment)
