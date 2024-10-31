from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.core.exceptions import ImproperlyConfigured
from django.utils.connection import BaseConnectionHandler
from django.utils.module_loading import import_string

if TYPE_CHECKING:
    from .base import HealthCheck
    from django_healthy._compat import Mapping, NotRequired, TypedDict

    class BackendConfig(TypedDict):
        BACKEND: str
        OPTIONS: NotRequired[Mapping[str, Any]]


class InvalidHealthCheckError(ImproperlyConfigured):
    pass


class HealthCheckHandler(BaseConnectionHandler):
    settings_name = "HEALTH_CHECKS"
    exception_class = InvalidHealthCheckError

    def create_connection(self, alias: str) -> HealthCheck:
        params: BackendConfig = self.settings[alias]
        backend: str = params["BACKEND"]
        options: Mapping[str, Any] = params.get("OPTIONS", {})

        try:
            factory = import_string(backend)
        except ImportError as e:
            msg = f"Could not find backend {backend!r}: {e}"
            raise InvalidHealthCheckError(msg) from e
        else:
            return factory(**options)


health_checks = HealthCheckHandler()
