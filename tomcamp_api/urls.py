from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from tomcamp_api.views import UserObtainTokenView


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]

        return schema


SchemaView = get_schema_view(
    openapi.Info(
        title="Tom.Camp API",
        default_version="v1",
        description="Tom.Camp API",
    ),
    generator_class=CustomSchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
    path('api-token-auth/', UserObtainTokenView.as_view()),
    path("api-auth/", include("rest_framework.urls")),
]
