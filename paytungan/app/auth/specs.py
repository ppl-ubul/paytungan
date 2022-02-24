from dataclasses import dataclass
from typing import List
from django.contrib.auth.models import User


@dataclass
class GetUserListSpec:
    user_ids: List[int]
    usernames: List[str]


@dataclass
class GetUserListReturnSpec:
    users: List[User]


@dataclass
class CreateUserSpec:
    username: str
    email: str
    password: str
