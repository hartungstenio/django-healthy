from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import timedelta
from timeit import default_timer as timer
from typing import Any

from django_healthy._compat import Mapping  # noqa: TCH001

from .base import HealthCheck, HealthStatus
from .handler import HealthCheckHandler, health_checks


@dataclass
class HealthReportEntry:
    status: HealthStatus
    duration: timedelta
    description: str | None = None
    exception: Exception | None = None
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    entries: Mapping[str, HealthReportEntry]
    status: HealthStatus
    total_duration: timedelta


class HealthCheckService:
    __slots__: tuple[str, ...] = ("_handler",)

    def __init__(self, handler: HealthCheckHandler | None = None):
        self._handler = handler or health_checks

    async def check_health(self) -> HealthReport:
        start_time: float = timer()
        task_map: dict[str, asyncio.Task[HealthReportEntry]] = {
            name: asyncio.create_task(self.run_health_check(health_check))
            for name, health_check in self._handler.items()
        }
        await asyncio.gather(*task_map.values())
        end_time: float = timer()

        entries: dict[str, HealthReportEntry] = {name: task.result() for name, task in task_map.items()}
        worst_case = min(entry.status.value for entry in entries.values())
        return HealthReport(
            entries=entries,
            status=HealthStatus(worst_case),
            total_duration=timedelta(seconds=end_time - start_time),
        )

    async def run_health_check(self, health_check: HealthCheck) -> HealthReportEntry:
        start_time: float = timer()
        result = await health_check.check_health()
        end_time: float = timer()

        return HealthReportEntry(
            status=result.status,
            duration=timedelta(seconds=end_time - start_time),
            description=result.description,
            exception=result.exception,
            data=result.data,
        )
