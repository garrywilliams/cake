from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

description = (
    "This is a fancy Cake Bakery API. You can find all sorts of cakes here!\n\n"
    "Welcome to the Cake Bakery API, a viral sensation in the world of digital bakeries! "
    "This API, crafted with love and a sprinkle of Python magic, allows you to interact "
    "with a virtual bakery's catalog of mouth-watering cakes. Whether you're looking to "
    "browse our extensive cake collection, add a new cake to our showcase, or even remove "
    "a cake from the menu, our API has got you covered.\n\n"
    "More details are available in the README file."
)


schema_view = get_schema_view(
    openapi.Info(
        title="Cake Bakery API",
        default_version="1.1.0",
        description=description,
        terms_of_service="http://example.com/terms/",
        contact=openapi.Contact(email="garry.p.williams@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger URLs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/", include("cake_server.urls")),
    path("prometheus/", include("django_prometheus.urls")),
]
