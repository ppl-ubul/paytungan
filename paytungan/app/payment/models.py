import uuid
from django.db import models

from paytungan.app.base.constants import PaymentStatus
from paytungan.app.base.models import BaseModel
from paytungan.app.split_bill.models import Bill


class Payment(BaseModel):
    bill = models.ForeignKey(
        Bill,
        related_name="payments",
        on_delete=models.PROTECT,
    )
    status = models.CharField(max_length=20, default=PaymentStatus.PENDING.value)
    method = models.CharField(max_length=64, blank=True, null=True)
    reference_no = models.CharField(max_length=256, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "payment"

    def __str__(self) -> str:
        return f"{str(self.id)} - {str(self.number)}"

    @property
    def number(self) -> str:
        date = self.created_at.strftime("%y%m%d")
        return f"PAY/{self.bill_id:05d}/{date}/{self.id:05d}"

    @property
    def amount(self) -> int:
        return self.bill.amount