from __future__ import annotations

from typing import ClassVar

from django.http import HttpRequest, HttpResponse
from django.template.response import TemplateResponse
from django.views import View

from .health_checks import HealthReport, HealthStatus, health_check_service


class LivenessView(View):
    http_method_names: ClassVar[list[str]] = [
        "get",
        "head",
        "options",
        "trace",
    ]

    async def get(self, request: HttpRequest) -> HttpResponse:  # noqa: ARG002
        return HttpResponse(HealthStatus.PASS, content_type="text/plain")


class HealthView(View):
    http_method_names: ClassVar[list[str]] = [
        "get",
        "head",
        "options",
        "trace",
    ]

    async def get(self, request: HttpRequest) -> HttpResponse:
        report: HealthReport = await health_check_service.check_health()
        context: dict[str, HealthReport] = {"report": report}
        return TemplateResponse(request, "django_healthy/report.html", context)
