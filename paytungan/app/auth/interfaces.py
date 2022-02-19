from abc import ABC, abstractmethod
from typing import List, Optional
from django.contrib.auth.models import User, Group

from .specs import GetUserListSpec


class IUserAccessor(ABC):
    @abstractmethod
    def get(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    def get_list(self, spec: GetUserListSpec) -> List[User]:
        raise NotImplementedError


class IUserServices(ABC):
    @abstractmethod
    def get(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    def get_list(self, spec: GetUserListSpec) -> List[User]:
        raise NotImplementedError
