import logging
from typing import Dict, List, Optional
from .models import User
from firebase_admin import initialize_app, auth, credentials
from injector import inject

from .interfaces import IUserAccessor, IFirebaseProvider
from .specs import (
    GetUserListSpec,
    CreateUserSpec,
    FirebaseDecodedToken,
    UpdateUserSpec,
)
from paytungan.app.common.constants import (
    DEFAULT_LOGGER,
    FIREBASE_PROJECT_ID,
    SERVICE_ACCOUNT_FILE,
)


class UserAccessor(IUserAccessor):
    def __init__(self) -> None:
        self.logger = logging.getLogger(DEFAULT_LOGGER)

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

        if spec.firebase_uids:
            queryset = queryset.filter(firebase_uid__in=spec.firebase_uids)

        return queryset

    def create_user(self, spec: CreateUserSpec) -> Optional[User]:
        try:
            new_user = User(
                firebase_uid=spec.firebase_uid,
                phone_number=spec.phone_number,
                username=spec.username,
                name=spec.name,
                email=spec.email,
                profil_image=spec.profil_image,
            )
            new_user.save()

            return new_user
        except Exception as e:
            self.logger.error(f"Error when try to create user with spec {spec}: {e}")
            return None
    
    def update_user(self, spec: UpdateUserSpec) -> Optional[User]:
        try:
            user = User.objects.get(pk=spec.firebase_uid)
            user = User(
                username=spec.username,
                name=spec.name,
                profil_image=spec.profil_image,
            )
            user.save()
            return user

        except Exception as e:
            self.logger.error(f"Error when try to update user with spec {spec}: {e}")
            return None


class FirebaseProvider(IFirebaseProvider):
    @inject
    def __init__(self) -> None:
        self._cred = None
        self._app = None
        self.logger = logging.getLogger(DEFAULT_LOGGER)

    def _get_app(self):
        if self._app:
            return self._app

        self._cred = credentials.Certificate(SERVICE_ACCOUNT_FILE)
        self._app = initialize_app(self._cred)
        return self._app

    def decode_token(self, token: str) -> Optional[FirebaseDecodedToken]:
        decoded_token: Dict[str, str]
        try:
            decoded_token = auth.verify_id_token(token, app=self._get_app())
        except Exception as e:
            self.logger.error(f"Error when verify token: {e}")

        if decoded_token.get("aud") != FIREBASE_PROJECT_ID:
            self.logger.info(f"Token not from {FIREBASE_PROJECT_ID} project")
            return None

        return FirebaseDecodedToken(
            user_id=decoded_token["user_id"],
            phone_number=decoded_token["phone_number"],
        )


class DummyFirebaseProvider(IFirebaseProvider):
    @inject
    def __init__(self) -> None:
        pass

    def decode_token(self, token: str) -> Optional[FirebaseDecodedToken]:
        return None
