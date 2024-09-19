from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django_healthy._compat import Self


class HealthStatus(Enum):
    UNHEALTHY = auto()
    DEGRADED = auto()
    HEALTHY = auto()


@dataclass
class HealthCheckResult:
    status: HealthStatus
    description: str | None = None
    exception: Exception | None = None
    data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def healthy(
        cls,
        description: str | None = None,
        exception: Exception | None = None,
        data: dict[str, Any] | None = None,
    ) -> Self:
        return cls(
            status=HealthStatus.HEALTHY,
            description=description,
            exception=exception,
            data=data or {},
        )

    @classmethod
    def degraded(
        cls,
        description: str | None = None,
        exception: Exception | None = None,
        data: dict[str, Any] | None = None,
    ) -> Self:
        return cls(
            status=HealthStatus.DEGRADED,
            description=description,
            exception=exception,
            data=data or {},
        )

    @classmethod
    def unhealthy(
        cls,
        description: str | None = None,
        exception: Exception | None = None,
        data: dict[str, Any] | None = None,
    ) -> Self:
        return cls(
            status=HealthStatus.UNHEALTHY,
            description=description,
            exception=exception,
            data=data or {},
        )


class HealthCheck(ABC):
    @abstractmethod
    async def check_health(self) -> HealthCheckResult: ...
