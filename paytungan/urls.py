from django.urls import include, path, re_path
from django.contrib import admin
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from paytungan.auth.views import UserViewSet


router = SimpleRouter(trailing_slash=False)
router.register("api/users", UserViewSet, basename="user")


swagger_info = openapi.Info(
    title="Paytungan API",
    default_version="v1",
    description="""
This is Paytungan API Backend Endpoint

The `swagger-ui` view can be found [here](/swagger).
The `ReDoc` view can be found [here](/redoc).
The swagger YAML document can be found [here](/swagger.yaml).

    """,  # noqa
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)

schema_view = get_schema_view(
    swagger_info,
    public=True,
    permission_classes=[permissions.AllowAny],
)

# urlpatterns required for settings values
required_urlpatterns = [
    path("admin/", admin.site.urls),
    # path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    re_path(
        r"^swagger(?P<format>.json|.yaml)$",
        schema_view.without_ui(cache_timeout=None),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=None),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/", schema_view.with_ui("redoc", cache_timeout=None), name="schema-redoc"
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + required_urlpatterns
