from django.urls import path

from .views import HealthView, LivenessView

app_name = "django_healthy"

urlpatterns = [
    path("ping/", LivenessView.as_view(), name="ping"),
    path("health/", HealthView.as_view(), name="health"),
]
