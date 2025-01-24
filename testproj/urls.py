from django.urls import include, path

urlpatterns = [
    path("health/", include("django_healthy.urls", namespace="django_healthy")),
]
