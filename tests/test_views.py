from http import HTTPStatus

import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestLivenessView:
    def test_get_ping(self, client):
        response = client.get(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_methods_not_allowed(self, method, client):
        django_client_method = getattr(client, method)

        response = django_client_method(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.asyncio
    async def test_get_ping_async(self, async_client):
        response = await async_client.get(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    async def test_methods_not_allowed_async(self, method, async_client):
        django_client_method = getattr(async_client, method)

        response = await django_client_method(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
