from unittest import mock

import pytest
from django.core.cache import caches

from django_healthy.health_checks import HealthStatus
from django_healthy.health_checks.cache import CacheHealthCheck


@pytest.mark.asyncio
class TestacheHealthCheck:
    async def test_check_health_with_working_cache(self):
        health_check = CacheHealthCheck()

        got = await health_check.check_health()

        assert got.status == HealthStatus.HEALTHY

    async def test_check_health_with_invalid_value(self):
        health_check = CacheHealthCheck(alias="dummy")

        got = await health_check.check_health()

        assert got.status == HealthStatus.DEGRADED
        assert "given" in got.data
        assert "got" in got.data

    async def test_check_health_with_broken_cache(self):
        health_check = CacheHealthCheck()
        cache = caches[health_check.alias]

        with mock.patch.object(cache, "aset", side_effect=RuntimeError):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY
        assert isinstance(got.exception, RuntimeError)
