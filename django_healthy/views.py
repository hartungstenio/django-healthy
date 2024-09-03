from __future__ import annotations

from typing import ClassVar

from django.http import HttpRequest, HttpResponse
from django.views import View


class LivenessView(View):
    http_method_names: ClassVar[list[str]] = [
        "get",
        "head",
        "options",
        "trace",
    ]

    async def get(self, request: HttpRequest) -> HttpResponse:  # noqa: ARG002
        return HttpResponse("Pong")
