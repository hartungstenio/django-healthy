from django_healthy.health_checks.base import HealthCheckResult, HealthStatus


class TestHealthCheckResult:
    def test_healthy_defaults(self):
        got = HealthCheckResult.healthy()

        assert got.status == HealthStatus.HEALTHY
        assert got.description is None
        assert got.exception is None
        assert got.data == {}

    def test_healthy_params(self, faker):
        given_description = faker.sentence()
        given_exception = Exception()
        given_data = faker.pydict()

        got = HealthCheckResult.healthy(
            description=given_description,
            exception=given_exception,
            data=given_data,
        )

        assert got.status == HealthStatus.HEALTHY
        assert got.description == given_description
        assert got.exception == given_exception
        assert got.data == given_data

    def test_degraded_defaults(self):
        got = HealthCheckResult.degraded()

        assert got.status == HealthStatus.DEGRADED
        assert got.description is None
        assert got.exception is None
        assert got.data == {}

    def test_degraded_params(self, faker):
        given_description = faker.sentence()
        given_exception = Exception()
        given_data = faker.pydict()

        got = HealthCheckResult.degraded(
            description=given_description,
            exception=given_exception,
            data=given_data,
        )

        assert got.status == HealthStatus.DEGRADED
        assert got.description == given_description
        assert got.exception == given_exception
        assert got.data == given_data

    def test_unhealthy_defaults(self):
        got = HealthCheckResult.unhealthy()

        assert got.status == HealthStatus.UNHEALTHY
        assert got.description is None
        assert got.exception is None
        assert got.data == {}

    def test_unhealthy_params(self, faker):
        given_description = faker.sentence()
        given_exception = Exception()
        given_data = faker.pydict()

        got = HealthCheckResult.unhealthy(
            description=given_description,
            exception=given_exception,
            data=given_data,
        )

        assert got.status == HealthStatus.UNHEALTHY
        assert got.description == given_description
        assert got.exception == given_exception
        assert got.data == given_data
