from injector import Injector

from .auth.modules import AuthModule


injector = Injector(
    [
        AuthModule,
    ]
)
