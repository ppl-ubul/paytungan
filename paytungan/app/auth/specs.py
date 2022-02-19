from dataclasses import dataclass
from typing import List


@dataclass
class GetUserListSpec:
    user_ids: List[int]
    usernames: List[str]
