from unittest import mock

import pytest
from django.db import DatabaseError

from django_healthy.health_checks import HealthStatus
from django_healthy.health_checks.db import DatabaseModelHealthCheck

pytestmark = pytest.mark.django_db


@pytest.mark.asyncio
class TestDatabaseModelHealthCheck:
    async def test_check_health_with_working_database(self):
        health_check = DatabaseModelHealthCheck()

        got = await health_check.check_health()

        assert got.status == HealthStatus.HEALTHY

    async def test_check_health_with_creation_error(self):
        health_check = DatabaseModelHealthCheck()

        with mock.patch("django_healthy.health_checks.db.Test.asave", side_effect=DatabaseError):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY

    async def test_check_health_with_update_error(self):
        health_check = DatabaseModelHealthCheck()

        with mock.patch("django_healthy.health_checks.db.Test.asave", side_effect=[True, DatabaseError]):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY

    async def test_check_health_with_deletion_error(self):
        health_check = DatabaseModelHealthCheck()

        with mock.patch("django_healthy.health_checks.db.Test.adelete", side_effect=DatabaseError):
            got = await health_check.check_health()

        assert got.status == HealthStatus.UNHEALTHY
