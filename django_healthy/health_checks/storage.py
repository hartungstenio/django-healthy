from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, ClassVar

from asgiref.sync import sync_to_async
from django.core.files.storage import Storage, storages
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from .base import HealthCheck, HealthCheckResult

if TYPE_CHECKING:
    from .types import MessageDict


class StorageHealthCheck(HealthCheck):
    __slots__: tuple[str, ...] = ("alias", "filename")
    messages: ClassVar[MessageDict] = {
        "missing": _("File missing"),
        "delete": _("Could not delete file"),
    }

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
                return HealthCheckResult.degraded(
                    description=self.messages["missing"].format(filename=filename),
                    data={"filename": filename},
                )

            await sync_to_async(storage.delete)(filename)
            exists = await sync_to_async(storage.exists)(filename)
            if exists:
                return HealthCheckResult.degraded(
                    description=self.messages["delete"].format(filename=filename),
                    data={"filename": filename},
                )
        except Exception as exc:  # noqa: BLE001
            return HealthCheckResult.unhealthy(exception=exc)
        else:
            return HealthCheckResult.healthy()
