from unittest import mock

import pytest
from django.db import DatabaseError

from django_healthy.health_checks import HealthStatus
from django_healthy.health_checks.db import DatabaseModelHealthCheck, DatabasePingHealthCheck

pytestmark = pytest.mark.django_db


@pytest.mark.asyncio
class TestDatabasePingHealthCheck:
    async def test_check_health_with_working_database(self):
        health_check = DatabasePingHealthCheck()

        got = await health_check.check_health()

        assert got.status == HealthStatus.PASS

    async def test_check_health_with_working_database_custom_query(self):
        health_check = DatabasePingHealthCheck(query="SELECT 1")

        got = await health_check.check_health()

        assert got.status == HealthStatus.PASS

    async def test_check_health_with_working_database_invalid_query(self):
        health_check = DatabasePingHealthCheck(query="INVALID QUERY")

        got = await health_check.check_health()

        assert got.status == HealthStatus.FAIL

    async def test_check_health_with_broken_database(self):
        health_check = DatabasePingHealthCheck(alias="dummy")

        got = await health_check.check_health()

        assert got.status == HealthStatus.FAIL


@pytest.mark.asyncio
class TestDatabaseModelHealthCheck:
    async def test_check_health_with_working_database(self):
        health_check = DatabaseModelHealthCheck()

        got = await health_check.check_health()

        assert got.status == HealthStatus.PASS

    async def test_check_health_with_creation_error(self):
        health_check = DatabaseModelHealthCheck()

        with mock.patch("django_healthy.health_checks.db.Test.asave", side_effect=DatabaseError):
            got = await health_check.check_health()

        assert got.status == HealthStatus.FAIL

    async def test_check_health_with_update_error(self):
        health_check = DatabaseModelHealthCheck()

        with mock.patch("django_healthy.health_checks.db.Test.asave", side_effect=[True, DatabaseError]):
            got = await health_check.check_health()

        assert got.status == HealthStatus.FAIL

    async def test_check_health_with_deletion_error(self):
        health_check = DatabaseModelHealthCheck()

        with mock.patch("django_healthy.health_checks.db.Test.adelete", side_effect=DatabaseError):
            got = await health_check.check_health()

        assert got.status == HealthStatus.FAIL
