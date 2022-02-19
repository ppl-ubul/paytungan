from typing import List, Optional
from django.contrib.auth.models import User, Group

from .interfaces import IUserAccessor
from .specs import GetUserListSpec


class UserAccessor(IUserAccessor):
    def get(self, user_id: int) -> Optional[User]:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        return user

    def get_list(self, spec: GetUserListSpec) -> List[User]:
        queryset = User.objects.all()

        if spec.user_ids:
            queryset = queryset.filter(id__in=spec.user_ids)

        if spec.usernames:
            queryset = queryset.filter(username__in=spec.usernames)

        return queryset
