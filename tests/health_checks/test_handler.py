import pytest
from django.conf import settings

from django_healthy.health_checks.cache import CacheHealthCheck
from django_healthy.health_checks.handler import HealthCheckHandler, InvalidHealthCheckError


class TestHealthCheckHandler:
    def test_with_custom_settings(self):
        handler = HealthCheckHandler(
            backends={
                "test": {
                    "BACKEND": "django_healthy.health_checks.cache.CacheHealthCheck",
                }
            }
        )
        items = set(handler.keys())

        assert items == {"test"}

    def test_with_default_settings(self):
        handler = HealthCheckHandler()
        items = set(handler.keys())

        assert items == set(settings.HEALTH_CHECKS)

    def test_get_existing_item(self):
        handler = HealthCheckHandler(
            backends={
                "test": {
                    "BACKEND": "django_healthy.health_checks.cache.CacheHealthCheck",
                }
            }
        )

        got = handler["test"]

        assert isinstance(got, CacheHealthCheck)

    def test_get_missing_item(self):
        handler = HealthCheckHandler(
            backends={
                "test": {
                    "BACKEND": "django_healthy.health_checks.cache.CacheHealthCheck",
                }
            }
        )

        with pytest.raises(InvalidHealthCheckError):
            handler["missing"]
