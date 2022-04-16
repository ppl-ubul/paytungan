from abc import ABC, abstractmethod
from typing import List, Optional

from .models import Payment
from .specs import (
    GetPaymentListSpec,
    PaymentDomain,
)


class IPaymentAccessor(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[Payment]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, spec: GetPaymentListSpec) -> List[Payment]:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj: PaymentDomain) -> Payment:
        raise NotImplementedError
