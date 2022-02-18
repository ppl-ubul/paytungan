from injector import Injector

from paytungan.auth.modules import AuthModule


injector = Injector(
    [
        AuthModule,
    ]
)
