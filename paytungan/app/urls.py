from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .auth.views import UserViewSet


router = SimpleRouter(trailing_slash=False)
router.register("api/users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
