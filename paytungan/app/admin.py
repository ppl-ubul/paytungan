from django.contrib import admin
from paytungan.app.payment.admin import PaymentAdmin

from paytungan.app.payment.models import Payment
from paytungan.app.auth.models import User
from paytungan.app.split_bill.admin import BillAdmin, SplitBillAdmin
from paytungan.app.split_bill.models import Bill, SplitBill

admin.site.register(User)
admin.site.register(Bill, BillAdmin)
admin.site.register(SplitBill, SplitBillAdmin)
admin.site.register(Payment, PaymentAdmin)
