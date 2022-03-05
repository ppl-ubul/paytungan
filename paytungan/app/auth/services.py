from typing import List, Optional
from .models import User
from injector import inject

from .interfaces import IFirebaseProvider, IUserAccessor
from .specs import GetUserListSpec, CreateUserSpec, UpdateUserSpec


class UserServices:
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
    
    def update_user(self, spec: UpdateUserSpec) -> Optional[User]:
        user = self.user_accessor.update_user(spec)
        return user


class AuthService:
    @inject
    def __init__(
        self,
        user_accessor: IUserAccessor,
        firebase_provider: IFirebaseProvider,
    ) -> None:
        self.user_accessor = user_accessor
        self.firebase_provider = firebase_provider

    def login(self, token: str) -> Optional[User]:
        decoded_token = self.firebase_provider.decode_token(token)
        user = self.user_accessor.get_list(
            GetUserListSpec(firebase_uids=[decoded_token.user_id])
        )

        if user:
            return user[0]

        return self.user_accessor.create_user(
            CreateUserSpec(
                firebase_uid=decoded_token.user_id,
                phone_number=decoded_token.phone_number,
            )
        )
