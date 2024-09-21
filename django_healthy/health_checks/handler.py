from __future__ import annotations

from typing import Any, Iterator, cast

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from django_healthy._compat import Mapping, MutableMapping, NotRequired, TypeAlias, TypedDict

from .base import HealthCheck


class InvalidHealthCheckError(ImproperlyConfigured):
    pass


class BackendConfig(TypedDict):
    BACKEND: str
    OPTIONS: NotRequired[Mapping[str, Any]]


HealthCheckConfig: TypeAlias = Mapping[str, BackendConfig]


class HealthCheckHandler(Mapping[str, HealthCheck]):
    __slots__: tuple[str, ...] = ("_backends", "_health_checks")

    def __init__(self, backends: HealthCheckConfig | None = None):
        self._backends = (
            backends if backends is not None else cast(HealthCheckConfig, getattr(settings, "HEALTH_CHECKS", {}))
        )
        self._health_checks: MutableMapping[str, HealthCheck] = {}

    def __getitem__(self, alias: str) -> HealthCheck:
        try:
            return self._health_checks[alias]
        except KeyError:
            try:
                params = self._backends[alias]
            except KeyError as exc:
                msg = f"Could not find config for '{alias}' in settings.HEALTH_CHECKS."
                raise InvalidHealthCheckError(msg) from exc
            else:
                health_check = self.create_health_check(params)
                self._health_checks[alias] = health_check
                return health_check

    def __iter__(self) -> Iterator[str]:
        return iter(self._backends)

    def __len__(self) -> int:
        return len(self._backends)

    def create_health_check(self, params: BackendConfig) -> HealthCheck:
        backend = params["BACKEND"]
        options = params.get("OPTIONS", {})

        try:
            factory = import_string(backend)
        except ImportError as e:
            msg = f"Could not find backend {backend!r}: {e}"
            raise InvalidHealthCheckError(msg) from e
        else:
            return factory(**options)


health_checks = HealthCheckHandler()
