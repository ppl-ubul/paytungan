from injector import Injector

from .auth.modules import AuthModule
from .split_bill.modules import SplitBillModule


injector = Injector(
    [
        AuthModule,
        SplitBillModule,
    ]
)
