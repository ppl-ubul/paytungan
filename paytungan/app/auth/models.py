from safedelete.models import SafeDeleteModel
from django.db import models


class User(SafeDeleteModel):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    profil_url = models.TextField(null=True, blank=True)
