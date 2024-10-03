from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from django.test import AsyncClient, Client
from django.urls import reverse

if TYPE_CHECKING:
    from django.http import HttpResponse

pytestmark = pytest.mark.django_db


class TestLivenessView:
    def test_get_ping(self, client: Client):
        response: HttpResponse = client.get(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_methods_not_allowed(self, method: str, client: Client):
        django_client_method = getattr(client, method)

        response: HttpResponse = django_client_method(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    @pytest.mark.asyncio
    async def test_get_ping_async(self, async_client: AsyncClient):
        response: HttpResponse = await async_client.get(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    async def test_methods_not_allowed_async(self, method: str, async_client: AsyncClient):
        django_client_method = getattr(async_client, method)

        response: HttpResponse = await django_client_method(reverse("django_healthy:ping"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


class TestHealthView:
    @pytest.mark.asyncio
    async def test_get_async(self, async_client: AsyncClient):
        response: HttpResponse = await async_client.get(reverse("django_healthy:health"))

        assert response.status_code == HTTPStatus.OK

    @pytest.mark.asyncio
    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    async def test_methods_not_allowed_async(self, method: str, async_client: AsyncClient):
        django_client_method = getattr(async_client, method)

        response: HttpResponse = await django_client_method(reverse("django_healthy:health"))

        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
