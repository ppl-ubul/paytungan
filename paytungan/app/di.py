from injector import Injector

from paytungan.app.payment.modules import PaymentModule
from paytungan.app.logging.modules import LoggingModule
from paytungan.app.auth.modules import AuthModule
from paytungan.app.split_bill.modules import SplitBillModule


injector = Injector(
    [
        AuthModule,
        SplitBillModule,
        LoggingModule,
        PaymentModule,
    ]
)
