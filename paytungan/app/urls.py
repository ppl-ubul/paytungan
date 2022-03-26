from rest_framework.routers import SimpleRouter
from django.urls import include, path

from .auth.views import UserViewSet, AuthViewSet
from .base.views import HealthCheckViewSet
from .split_bill.views import SplitBillViewSet, BillViewSet


router = SimpleRouter(trailing_slash=False)
router.register("health-check", HealthCheckViewSet, basename="healthcheck")
router.register("api/users", UserViewSet, basename="user")
router.register("api/authentication", AuthViewSet, basename="authentication")
router.register("api/split-bills", SplitBillViewSet, basename="split-bill")
router.register("api/bills", BillViewSet, basename="bill")

urlpatterns = [
    path("", include(router.urls)),
]
