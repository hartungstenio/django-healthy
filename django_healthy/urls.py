from django.urls import path

from .views import LivenessView

app_name = "django_healthy"

urlpatterns = [
    path("ping/", LivenessView.as_view(), name="ping"),
]
