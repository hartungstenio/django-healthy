from django.urls import path

from .views import HealthView, LivenessView

app_name = "django_healthy"

urlpatterns = [
    path("", HealthView.as_view(), name="health"),
    path("alive/", LivenessView.as_view(), name="ping"),
]
