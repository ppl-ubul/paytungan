from abc import ABC, abstractmethod
from typing import List, Optional
from .models import User

from .specs import (
    GetUserListSpec,
    CreateUserSpec,
    FirebaseDecodedToken,
    UpdateUserSpec,
)


class IUserAccessor(ABC):
    @abstractmethod
    def get(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def get_list(self, spec: GetUserListSpec) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, spec: CreateUserSpec) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, spec: UpdateUserSpec) -> Optional[User]:
        raise NotImplementedError


class IFirebaseProvider(ABC):
    @abstractmethod
    def decode_token(self, token: str) -> FirebaseDecodedToken:
        raise NotImplementedError
