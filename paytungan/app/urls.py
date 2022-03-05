from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .auth.views import UserViewSet, AuthViewSet
from .common.views import HealthCheckViewSet


router = SimpleRouter(trailing_slash=False)
router.register("health-check", HealthCheckViewSet, basename="healthcheck")
router.register("api/users", UserViewSet, basename="user")
router.register("api/authentication", AuthViewSet, basename="authentication")

urlpatterns = [
    path("", include(router.urls)),
]
