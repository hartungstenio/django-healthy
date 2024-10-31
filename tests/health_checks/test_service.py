import pytest
from django.conf import settings

from django_healthy.health_checks import HealthStatus
from django_healthy.health_checks.handler import HealthCheckHandler
from django_healthy.health_checks.service import HealthCheckService

pytestmark = pytest.mark.django_db


@pytest.mark.asyncio
class TestHealthCheckService:
    async def test_with_default_handler(self):
        service = HealthCheckService()

        got = await service.check_health()

        assert got.status == HealthStatus.HEALTHY
        assert set(got.entries.keys()) == set(settings.HEALTH_CHECKS.keys())

    async def test_with_custom_handler(self):
        service = HealthCheckService(
            HealthCheckHandler(
                {
                    "test": {
                        "BACKEND": "django_healthy.health_checks.cache.CacheHealthCheck",
                    }
                }
            )
        )

        got = await service.check_health()

        assert got.status == HealthStatus.HEALTHY
        assert set(got.entries.keys()) == {"test"}

    async def test_with_unhealthy_service(self):
        service = HealthCheckService(
            HealthCheckHandler(
                {
                    "test": {
                        "BACKEND": "django_healthy.health_checks.db.DatabasePingHealthCheck",
                        "OPTIONS": {
                            "alias": "dummy",
                        },
                    }
                }
            )
        )

        got = await service.check_health()

        assert got.status == HealthStatus.UNHEALTHY
        assert set(got.entries.keys()) == {"test"}

    async def test_with_multiple_service_status_gets_worst_case(self):
        service = HealthCheckService(
            HealthCheckHandler(
                {
                    "healthy": {
                        "BACKEND": "django_healthy.health_checks.db.DatabasePingHealthCheck",
                        "OPTIONS": {
                            "alias": "default",
                        },
                    },
                    "unhealthy": {
                        "BACKEND": "django_healthy.health_checks.db.DatabasePingHealthCheck",
                        "OPTIONS": {
                            "alias": "dummy",
                        },
                    },
                }
            )
        )

        got = await service.check_health()

        assert got.status == HealthStatus.UNHEALTHY
        assert set(got.entries.keys()) == {"healthy", "unhealthy"}
