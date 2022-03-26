from django.contrib import admin

from .auth.models import User
from .split_bill.models import Bill, SplitBill

admin.site.register(User)
admin.site.register(Bill)
admin.site.register(SplitBill)
