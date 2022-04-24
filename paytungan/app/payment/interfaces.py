from abc import ABC, abstractmethod
from typing import List, Optional
from xendit.models.invoice import Invoice

from .models import Payment
from .specs import (
    CreateXenditInvoiceSpec,
    GetPaymentListSpec,
    InvoiceDomain,
    PaymentDomain,
    UpdatePaymentSpec,
)


class IPaymentAccessor(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[PaymentDomain]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, spec: GetPaymentListSpec) -> List[Payment]:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj: PaymentDomain) -> PaymentDomain:
        raise NotImplementedError

    @abstractmethod
    def update(self, spec: UpdatePaymentSpec) -> PaymentDomain:
        raise NotImplementedError

    @abstractmethod
    def get_by_bill_id(self, bill_id: int) -> Optional[PaymentDomain]:
        raise NotImplementedError


class IXenditProvider(ABC):
    @abstractmethod
    def create_invoice(self, spec: CreateXenditInvoiceSpec) -> InvoiceDomain:
        raise NotImplementedError

    @abstractmethod
    def get_invoice(self, invoice_id: str) -> InvoiceDomain:
        raise NotImplementedError
