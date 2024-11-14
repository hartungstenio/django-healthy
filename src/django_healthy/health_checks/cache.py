from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.core.cache import caches
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .base import HealthCheck, HealthCheckResult

if TYPE_CHECKING:
    from .types import MessageDict


class CacheHealthCheck(HealthCheck):
    __slots__: tuple[str, ...] = ("alias", "key_prefix")
    messages: ClassVar[MessageDict] = {
        "unexpected": _("Got unexpected value"),
    }

    def __init__(self, alias: str = "default", key_prefix: str = "django_healthy"):
        self.alias = alias
        self.key_prefix = key_prefix

    async def check_health(self) -> HealthCheckResult:
        cache = caches[self.alias]
        given = get_random_string(10)
        key = f"{self.key_prefix}_{get_random_string(5)}"

        try:
            await cache.aset(key, given)
            got = await cache.aget(key)
        except Exception as exc:  # noqa: BLE001
            return HealthCheckResult.unhealthy(exception=exc)
        else:
            if got != given:
                return HealthCheckResult.degraded(
                    description=self.messages["unexpected"].format(given=given, got=got),
                    data={"given": given, "got": got},
                )
            return HealthCheckResult.healthy()
