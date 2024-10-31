from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, cast

from asgiref.sync import sync_to_async
from django.db import DatabaseError, connections
from django.db.backends.base.base import BaseDatabaseWrapper as DjangoDatabaseWrapper
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .base import HealthCheck, HealthCheckResult
from django_healthy.models import Test

if TYPE_CHECKING:
    from .types import MessageDict


class DatabasePingHealthCheck(HealthCheck):
    __slots__: tuple[str, ...] = ("alias", "query")

    def __init__(self, alias: str = "default", query: str = "--ping"):
        self.alias = alias
        self.query = query

    async def check_health(self) -> HealthCheckResult:
        try:
            await sync_to_async(self._perform_health_check)()
        except Exception as exc:  # noqa: BLE001
            return HealthCheckResult.unhealthy(exception=exc)
        else:
            return HealthCheckResult.healthy()

    def _perform_health_check(self) -> None:
        connection: DjangoDatabaseWrapper = cast(DjangoDatabaseWrapper, connections[self.alias])

        with connection.cursor() as cursor:
            cursor.execute(self.query)


class DatabaseModelHealthCheck(HealthCheck):
    __slots__: tuple[str, ...] = ("alias",)
    messages: ClassVar[MessageDict] = {
        "insert": _("Could not insert"),
        "update": _("Could not update"),
        "delete": _("Could not delete"),
    }

    def __init__(self, alias: str | None = None):
        self.alias = alias

    async def check_health(self) -> HealthCheckResult:
        instance = Test(summary=get_random_string(100))
        try:
            await instance.asave(using=self.alias)
        except DatabaseError as exc:
            return HealthCheckResult.unhealthy(description=self.messages["insert"], exception=exc)

        try:
            instance.summary = get_random_string(100)
            await instance.asave(using=self.alias)
        except DatabaseError as exc:
            return HealthCheckResult.unhealthy(description=self.messages["update"], exception=exc)

        try:
            await instance.adelete(using=self.alias)
        except DatabaseError as exc:
            return HealthCheckResult.unhealthy(description=self.messages["delete"], exception=exc)

        return HealthCheckResult.healthy()
