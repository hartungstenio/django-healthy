from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import auto
from typing import TYPE_CHECKING, Any

from django_healthy._compat import StrEnum

if TYPE_CHECKING:
    from django_healthy._compat import Self


class HealthStatus(StrEnum):
    FAIL = auto()
    WARN = auto()
    PASS = auto()


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
            status=HealthStatus.PASS,
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
            status=HealthStatus.WARN,
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
            status=HealthStatus.FAIL,
            description=description,
            exception=exception,
            data=data or {},
        )


class HealthCheck(ABC):
    __slots__: tuple[()] = ()

    @abstractmethod
    async def check_health(self) -> HealthCheckResult: ...
