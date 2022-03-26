from safedelete.models import SafeDeleteModel
from django.db import models
from django.db.models import Q


class User(SafeDeleteModel):
    firebase_uid = models.CharField(max_length=512)
    phone_number = models.CharField(max_length=50)
    username = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    profil_image = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(
                fields=["firebase_uid"],
                condition=Q(deleted__isnull=True),
                name="unique_firebase_uid_if_not_deleted",
            ),
            models.UniqueConstraint(
                fields=["username"],
                condition=Q(deleted__isnull=True, username__isnull=False),
                name="unique_username_if_not_deleted",
            ),
        ]
        indexes = [
            models.Index(
                fields=["firebase_uid"],
                name="index_user_firebase_uid",
            ),
            models.Index(
                fields=["username"],
                name="index_user_username",
            ),
        ]

    @property
    def is_onboarding(self) -> bool:
        return not (self.username and self.name)

    def __str__(self) -> str:
        return f"{str(self.username)} - {str(self.id)}"
