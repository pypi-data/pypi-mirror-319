# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import TopicListResponse
from tests.utils import assert_matches_type
from avido.pagination import SyncOffsetPagination, AsyncOffsetPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Avido) -> None:
        topic = client.topics.list()
        assert_matches_type(SyncOffsetPagination[TopicListResponse], topic, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Avido) -> None:
        topic = client.topics.list(
            limit=25,
            order_by="createdAt",
            order_dir="asc",
            skip=0,
            title="code quality",
        )
        assert_matches_type(SyncOffsetPagination[TopicListResponse], topic, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Avido) -> None:
        response = client.topics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = response.parse()
        assert_matches_type(SyncOffsetPagination[TopicListResponse], topic, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Avido) -> None:
        with client.topics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = response.parse()
            assert_matches_type(SyncOffsetPagination[TopicListResponse], topic, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTopics:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.list()
        assert_matches_type(AsyncOffsetPagination[TopicListResponse], topic, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncAvido) -> None:
        topic = await async_client.topics.list(
            limit=25,
            order_by="createdAt",
            order_dir="asc",
            skip=0,
            title="code quality",
        )
        assert_matches_type(AsyncOffsetPagination[TopicListResponse], topic, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncAvido) -> None:
        response = await async_client.topics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic = await response.parse()
        assert_matches_type(AsyncOffsetPagination[TopicListResponse], topic, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncAvido) -> None:
        async with async_client.topics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic = await response.parse()
            assert_matches_type(AsyncOffsetPagination[TopicListResponse], topic, path=["response"])

        assert cast(Any, response.is_closed) is True
