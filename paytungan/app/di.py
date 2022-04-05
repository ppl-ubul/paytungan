from injector import Injector

from .logging.modules import LoggingModule
from .auth.modules import AuthModule
from .split_bill.modules import SplitBillModule


injector = Injector(
    [
        AuthModule,
        SplitBillModule,
        LoggingModule,
    ]
)
