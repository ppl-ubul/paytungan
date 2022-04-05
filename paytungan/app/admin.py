from django.contrib import admin

from .split_bill.admin import BillAdmin, SplitBillAdmin
from .auth.models import User
from .split_bill.models import Bill, SplitBill

admin.site.register(User)
admin.site.register(Bill, BillAdmin)
admin.site.register(SplitBill, SplitBillAdmin)
