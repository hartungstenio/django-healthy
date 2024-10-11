from __future__ import annotations

from io import StringIO

from asgiref.sync import sync_to_async
from django.core.files.storage import Storage, storages
from django.utils.crypto import get_random_string

from .base import HealthCheck, HealthCheckResult


class StorageHealthCheck(HealthCheck):
    __slots__: tuple[str, ...] = ("alias", "filename")

    def __init__(self, alias: str = "default", filename: str = "healthy_test_file.txt"):
        self.alias = alias
        self.filename = filename

    async def check_health(self) -> HealthCheckResult:
        storage: Storage = storages[self.alias]
        given: str = get_random_string(100)

        try:
            filename = await sync_to_async(storage.get_available_name)(self.filename)
            await sync_to_async(storage.save)(filename, StringIO(given))

            exists = await sync_to_async(storage.exists)(filename)
            if not exists:
                return HealthCheckResult.degraded(description="File missing", data={"filename": filename})

            await sync_to_async(storage.delete)(filename)
            exists = await sync_to_async(storage.exists)(filename)
            if exists:
                return HealthCheckResult.degraded(description="Could not delete file", data={"filename": filename})
        except Exception as exc:  # noqa: BLE001
            return HealthCheckResult.unhealthy(exception=exc)
        else:
            return HealthCheckResult.healthy()
