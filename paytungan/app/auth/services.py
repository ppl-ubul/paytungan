from typing import List, Optional
from django.contrib.auth.models import User
from injector import inject

from .interfaces import IUserAccessor, IUserServices
from .specs import GetUserListSpec, CreateUserSpec


class UserServices(IUserServices):
    @inject
    def __init__(self, user_accessor: IUserAccessor) -> None:
        self.user_accessor = user_accessor

    def get(self, user_id: int) -> Optional[User]:
        return self.user_accessor.get(user_id)

    def get_list(self, spec: GetUserListSpec) -> List[User]:
        return self.user_accessor.get_list(spec)

    def create_user(self, spec: CreateUserSpec) -> Optional[User]:
        user = self.user_accessor.create_user(spec)
        return user
