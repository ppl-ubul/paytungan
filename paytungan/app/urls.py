from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .auth.views import UserViewSet, AuthViewSet


router = SimpleRouter(trailing_slash=False)
router.register("api/users", UserViewSet, basename="user")
router.register("api/authentication", AuthViewSet, basename="authentication")

urlpatterns = [
    path("", include(router.urls)),
]
