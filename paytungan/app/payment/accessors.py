from typing import List, Optional
from paytungan.app.common.utils import ObjectMapperUtil

from paytungan.app.split_bill.models import Bill
from .specs import GetPaymentListSpec, PaymentDomain
from .interfaces import IPaymentAccessor
from .models import Payment


class PaymentAccessor(IPaymentAccessor):
    def get(self, id: int) -> Optional[Payment]:
        try:
            payment = Payment.objects.get(pk=id)
        except Payment.DoesNotExist:
            return None

        return payment

    def get_list(self, spec: GetPaymentListSpec) -> List[Payment]:
        queryset = Payment.objects.all()

        if spec.user_id:
            bill_ids = list(
                Bill.objects.queryset.filter(user_id=spec.user_id)
                .values_list("id", flat=True)
                .distinct()
            )
            spec.bill_ids.extend(bill_ids)

        if spec.bill_ids:
            queryset = queryset.filter(bill_id=spec.bill_id)

        if spec.status:
            queryset = queryset.filter(status=spec.status)

        return queryset

    def create(self, obj: PaymentDomain) -> Payment:
        payment = self._convert_to_model(obj=obj, is_create=True)
        payment.save()
        return payment

    @staticmethod
    def _convert_to_model(obj: PaymentDomain, is_create: bool) -> Payment:
        return Payment(
            id=None if is_create else obj.id,
            user_id=obj.user_id,
            split_bill_id=obj.split_bill_id,
            status=obj.status,
            details=obj.details,
            **ObjectMapperUtil.default_model_creation_params()
        )

    def _convert_to_model_list(
        self, objects: List[PaymentDomain], is_create: bool
    ) -> List[Payment]:
        return [self._convert_to_model(obj, is_create) for obj in objects]
