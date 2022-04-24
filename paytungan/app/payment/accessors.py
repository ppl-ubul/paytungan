from typing import List, Optional
from xendit import Xendit, Invoice
from xendit.xendit_error import XenditError

from paytungan.app.common.exceptions import NotFoundException
from paytungan.app.common.utils import ObjectMapperUtil
from paytungan.app.base.constants import XENDIT_API_KEY
from paytungan.app.split_bill.models import Bill
from .specs import (
    CreateXenditInvoiceSpec,
    GetPaymentListSpec,
    InvoiceDomain,
    PaymentDomain,
    UpdatePaymentSpec,
)
from .interfaces import IPaymentAccessor, IXenditProvider
from .models import Payment


class PaymentAccessor(IPaymentAccessor):
    def get(self, id: int) -> Optional[PaymentDomain]:
        try:
            payment = Payment.objects.get(pk=id)
        except Payment.DoesNotExist:
            return None

        return self._convert_to_domain(payment)

    def get_list(self, spec: GetPaymentListSpec) -> List[Payment]:
        queryset = Payment.objects.all()

        if spec.user_id:
            bill_ids = list(
                Bill.objects.filter(user_id=spec.user_id)
                .values_list("id", flat=True)
                .distinct()
            )
            spec.bill_ids.extend(bill_ids)

        if spec.bill_ids:
            queryset = queryset.filter(bill_id__in=spec.bill_ids)

        if spec.status:
            queryset = queryset.filter(status=spec.status)

        return queryset

    def create(self, obj: PaymentDomain) -> PaymentDomain:
        payment = self._convert_to_model(obj=obj, is_create=True)
        payment.save()
        return self._convert_to_domain(payment)

    def update(self, spec: UpdatePaymentSpec) -> PaymentDomain:
        payment = self._convert_to_model(obj=spec.obj, is_create=False)
        payment.save(update_fields=spec.updated_fields)

        return self._convert_to_domain(payment)

    @staticmethod
    def _convert_to_domain(obj: Payment) -> PaymentDomain:
        return ObjectMapperUtil.map(obj, PaymentDomain)

    @staticmethod
    def _convert_to_model(obj: PaymentDomain, is_create: bool) -> Payment:
        return Payment(
            id=None if is_create else obj.id,
            bill_id=obj.bill_id,
            status=obj.status,
            method=obj.method,
            reference_no=obj.reference_no,
            paid_at=obj.paid_at,
            expiry_date=obj.expiry_date,
            **ObjectMapperUtil.default_model_creation_params(),
        )

    def _convert_to_model_list(
        self, objects: List[PaymentDomain], is_create: bool
    ) -> List[Payment]:
        return [self._convert_to_model(obj, is_create) for obj in objects]


class XenditProvider(IXenditProvider):
    def __init__(self) -> None:
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client

        self._client = Xendit(api_key=XENDIT_API_KEY)
        return self._client

    def get_invoice(self, invoice_id: str) -> InvoiceDomain:
        client = self._get_client()

        try:
            invoice = client.Invoice.get(
                invoice_id=invoice_id,
            )
        except XenditError:
            raise NotFoundException(f"Invoice with id: {invoice_id} is not found.")

        return self._convert_invoice_domain(invoice)

    def create_invoice(self, spec: CreateXenditInvoiceSpec) -> InvoiceDomain:
        client = self._get_client()
        invoice = client.Invoice.create(
            external_id=spec.external_id,
            amount=spec.amount,
            payer_email=spec.payer_email,
            description=spec.description,
            should_send_email=True,
            success_redirect_url=spec.success_redirect_url,
            failure_redirect_url=spec.failure_redirect_url,
        )

        return self._convert_invoice_domain(invoice)

    @staticmethod
    def _convert_invoice_domain(obj: Invoice) -> InvoiceDomain:
        return ObjectMapperUtil.map(vars(obj), InvoiceDomain)
