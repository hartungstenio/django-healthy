from unittest import mock

import pytest
from django.core.files.storage import storages

from django_healthy.health_checks import HealthStatus
from django_healthy.health_checks.storage import StorageHealthCheck


@pytest.mark.asyncio
class TestStorageHealthCheck:
    async def test_with_working_storage(self):
        health_check = StorageHealthCheck()

        got = await health_check.check_health()

        assert got.status == HealthStatus.HEALTHY

    async def test_without_saving(self):
        health_check = StorageHealthCheck()
        storage = storages[health_check.alias]

        with mock.patch.object(storage, "save"):
            got = await health_check.check_health()

        assert got.status == HealthStatus.DEGRADED
        assert "filename" in got.data

    async def test_without_deleting(self):
        health_check = StorageHealthCheck()
        storage = storages[health_check.alias]

        with mock.patch.object(storage, "delete"):
            got = await health_check.check_health()

        assert got.status == HealthStatus.DEGRADED
        assert "filename" in got.data

    async def test_with_save_error(self):
        health_check = StorageHealthCheck()
        storage = storages[health_check.alias]

        with mock.patch.object(storage, "save", side_effect=Exception):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY

    async def test_with_delete_error(self):
        health_check = StorageHealthCheck()
        storage = storages[health_check.alias]

        with mock.patch.object(storage, "delete", side_effect=Exception):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY

    async def test_with_exists_error(self):
        health_check = StorageHealthCheck()
        storage = storages[health_check.alias]

        with mock.patch.object(storage, "exists", side_effect=Exception):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY
