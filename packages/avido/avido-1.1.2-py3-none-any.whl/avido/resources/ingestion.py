# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import ingestion_ingest_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.ingestion_ingest_response import IngestionIngestResponse

__all__ = ["IngestionResource", "AsyncIngestionResource"]


class IngestionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> IngestionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return IngestionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> IngestionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return IngestionResourceWithStreamingResponse(self)

    def ingest(
        self,
        *,
        events: Iterable[ingestion_ingest_params.Event],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IngestionIngestResponse:
        """
        Receives an array of events describing LLM usage, tool calls, threads, retriever
        queries, or logs. Each event is typed by its `type` field (llm, tool, etc.).

        Args:
          events: An array of typed events (LLM usage, tool calls, threads, retriever queries, or
              logs).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/ingest",
            body=maybe_transform({"events": events}, ingestion_ingest_params.IngestionIngestParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IngestionIngestResponse,
        )


class AsyncIngestionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncIngestionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncIngestionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncIngestionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncIngestionResourceWithStreamingResponse(self)

    async def ingest(
        self,
        *,
        events: Iterable[ingestion_ingest_params.Event],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> IngestionIngestResponse:
        """
        Receives an array of events describing LLM usage, tool calls, threads, retriever
        queries, or logs. Each event is typed by its `type` field (llm, tool, etc.).

        Args:
          events: An array of typed events (LLM usage, tool calls, threads, retriever queries, or
              logs).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/ingest",
            body=await async_maybe_transform({"events": events}, ingestion_ingest_params.IngestionIngestParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=IngestionIngestResponse,
        )


class IngestionResourceWithRawResponse:
    def __init__(self, ingestion: IngestionResource) -> None:
        self._ingestion = ingestion

        self.ingest = to_raw_response_wrapper(
            ingestion.ingest,
        )


class AsyncIngestionResourceWithRawResponse:
    def __init__(self, ingestion: AsyncIngestionResource) -> None:
        self._ingestion = ingestion

        self.ingest = async_to_raw_response_wrapper(
            ingestion.ingest,
        )


class IngestionResourceWithStreamingResponse:
    def __init__(self, ingestion: IngestionResource) -> None:
        self._ingestion = ingestion

        self.ingest = to_streamed_response_wrapper(
            ingestion.ingest,
        )


class AsyncIngestionResourceWithStreamingResponse:
    def __init__(self, ingestion: AsyncIngestionResource) -> None:
        self._ingestion = ingestion

        self.ingest = async_to_streamed_response_wrapper(
            ingestion.ingest,
        )
