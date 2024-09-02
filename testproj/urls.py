from django.urls import include, path

urlpatterns = [
    path("", include("django_healthy.urls", namespace="django_healthy")),
]
