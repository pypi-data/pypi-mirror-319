# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import IngestionIngestResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIngestion:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_ingest(self, client: Avido) -> None:
        ingestion = client.ingestion.ingest(
            events=[
                {
                    "timestamp": "2025-01-05T12:34:56.789Z",
                    "type": "llm",
                },
                {
                    "timestamp": "2025-01-05T12:35:06.123Z",
                    "type": "tool",
                },
            ],
        )
        assert_matches_type(IngestionIngestResponse, ingestion, path=["response"])

    @parametrize
    def test_raw_response_ingest(self, client: Avido) -> None:
        response = client.ingestion.with_raw_response.ingest(
            events=[
                {
                    "timestamp": "2025-01-05T12:34:56.789Z",
                    "type": "llm",
                },
                {
                    "timestamp": "2025-01-05T12:35:06.123Z",
                    "type": "tool",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ingestion = response.parse()
        assert_matches_type(IngestionIngestResponse, ingestion, path=["response"])

    @parametrize
    def test_streaming_response_ingest(self, client: Avido) -> None:
        with client.ingestion.with_streaming_response.ingest(
            events=[
                {
                    "timestamp": "2025-01-05T12:34:56.789Z",
                    "type": "llm",
                },
                {
                    "timestamp": "2025-01-05T12:35:06.123Z",
                    "type": "tool",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ingestion = response.parse()
            assert_matches_type(IngestionIngestResponse, ingestion, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncIngestion:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_ingest(self, async_client: AsyncAvido) -> None:
        ingestion = await async_client.ingestion.ingest(
            events=[
                {
                    "timestamp": "2025-01-05T12:34:56.789Z",
                    "type": "llm",
                },
                {
                    "timestamp": "2025-01-05T12:35:06.123Z",
                    "type": "tool",
                },
            ],
        )
        assert_matches_type(IngestionIngestResponse, ingestion, path=["response"])

    @parametrize
    async def test_raw_response_ingest(self, async_client: AsyncAvido) -> None:
        response = await async_client.ingestion.with_raw_response.ingest(
            events=[
                {
                    "timestamp": "2025-01-05T12:34:56.789Z",
                    "type": "llm",
                },
                {
                    "timestamp": "2025-01-05T12:35:06.123Z",
                    "type": "tool",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ingestion = await response.parse()
        assert_matches_type(IngestionIngestResponse, ingestion, path=["response"])

    @parametrize
    async def test_streaming_response_ingest(self, async_client: AsyncAvido) -> None:
        async with async_client.ingestion.with_streaming_response.ingest(
            events=[
                {
                    "timestamp": "2025-01-05T12:34:56.789Z",
                    "type": "llm",
                },
                {
                    "timestamp": "2025-01-05T12:35:06.123Z",
                    "type": "tool",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ingestion = await response.parse()
            assert_matches_type(IngestionIngestResponse, ingestion, path=["response"])

        assert cast(Any, response.is_closed) is True
