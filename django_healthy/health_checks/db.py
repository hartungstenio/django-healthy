from __future__ import annotations

from django.db import DatabaseError
from django.utils.crypto import get_random_string

from django_healthy.models import Test

from .base import HealthCheck, HealthCheckResult


class DatabaseModelHealthCheck(HealthCheck):
    __slots__: tuple[str, ...] = ("alias",)

    def __init__(self, alias: str | None = None):
        self.alias = alias

    async def check_health(self) -> HealthCheckResult:
        instance = Test(summary=get_random_string(100))
        try:
            await instance.asave(using=self.alias)
        except DatabaseError as exc:
            return HealthCheckResult.unhealthy(description="Could not insert", exception=exc)

        try:
            instance.summary = get_random_string(100)
            await instance.asave(using=self.alias)
        except DatabaseError as exc:
            return HealthCheckResult.unhealthy(description="Could not update", exception=exc)

        try:
            await instance.adelete(using=self.alias)
        except DatabaseError as exc:
            return HealthCheckResult.unhealthy(description="Could not delete", exception=exc)

        return HealthCheckResult.healthy()
