# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import ThreadCreateResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Avido) -> None:
        thread = client.threads.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ThreadCreateResponse, thread, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Avido) -> None:
        thread = client.threads.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
            evaluation_id="789e4567-e89b-12d3-a456-426614174000",
            message={"content": "bar"},
            metadata={
                "userId": "bar",
                "context": "bar",
            },
        )
        assert_matches_type(ThreadCreateResponse, thread, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Avido) -> None:
        response = client.threads.with_raw_response.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = response.parse()
        assert_matches_type(ThreadCreateResponse, thread, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Avido) -> None:
        with client.threads.with_streaming_response.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = response.parse()
            assert_matches_type(ThreadCreateResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncThreads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncAvido) -> None:
        thread = await async_client.threads.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ThreadCreateResponse, thread, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncAvido) -> None:
        thread = await async_client.threads.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
            evaluation_id="789e4567-e89b-12d3-a456-426614174000",
            message={"content": "bar"},
            metadata={
                "userId": "bar",
                "context": "bar",
            },
        )
        assert_matches_type(ThreadCreateResponse, thread, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAvido) -> None:
        response = await async_client.threads.with_raw_response.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        thread = await response.parse()
        assert_matches_type(ThreadCreateResponse, thread, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAvido) -> None:
        async with async_client.threads.with_streaming_response.create(
            application_id="456e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            thread = await response.parse()
            assert_matches_type(ThreadCreateResponse, thread, path=["response"])

        assert cast(Any, response.is_closed) is True
