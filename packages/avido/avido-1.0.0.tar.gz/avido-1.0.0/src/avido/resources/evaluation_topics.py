# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import evaluation_topic_create_params
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
from ..types.evaluation_topic import EvaluationTopic

__all__ = ["EvaluationTopicsResource", "AsyncEvaluationTopicsResource"]


class EvaluationTopicsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationTopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return EvaluationTopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationTopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return EvaluationTopicsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        title: str,
        benchmark: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationTopic:
        """
        Creates a new evaluation topic.

        Args:
          title: Title of the evaluation topic

          benchmark: Optional benchmark score for this topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/topics",
            body=maybe_transform(
                {
                    "title": title,
                    "benchmark": benchmark,
                },
                evaluation_topic_create_params.EvaluationTopicCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationTopic,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationTopic:
        """
        Retrieves detailed information about a specific evaluation topic.

        Args:
          id: The unique identifier of the evaluation topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v0/topics/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationTopic,
        )


class AsyncEvaluationTopicsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationTopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationTopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationTopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncEvaluationTopicsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        title: str,
        benchmark: Optional[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationTopic:
        """
        Creates a new evaluation topic.

        Args:
          title: Title of the evaluation topic

          benchmark: Optional benchmark score for this topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/topics",
            body=await async_maybe_transform(
                {
                    "title": title,
                    "benchmark": benchmark,
                },
                evaluation_topic_create_params.EvaluationTopicCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationTopic,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationTopic:
        """
        Retrieves detailed information about a specific evaluation topic.

        Args:
          id: The unique identifier of the evaluation topic

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v0/topics/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationTopic,
        )


class EvaluationTopicsResourceWithRawResponse:
    def __init__(self, evaluation_topics: EvaluationTopicsResource) -> None:
        self._evaluation_topics = evaluation_topics

        self.create = to_raw_response_wrapper(
            evaluation_topics.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluation_topics.retrieve,
        )


class AsyncEvaluationTopicsResourceWithRawResponse:
    def __init__(self, evaluation_topics: AsyncEvaluationTopicsResource) -> None:
        self._evaluation_topics = evaluation_topics

        self.create = async_to_raw_response_wrapper(
            evaluation_topics.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluation_topics.retrieve,
        )


class EvaluationTopicsResourceWithStreamingResponse:
    def __init__(self, evaluation_topics: EvaluationTopicsResource) -> None:
        self._evaluation_topics = evaluation_topics

        self.create = to_streamed_response_wrapper(
            evaluation_topics.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluation_topics.retrieve,
        )


class AsyncEvaluationTopicsResourceWithStreamingResponse:
    def __init__(self, evaluation_topics: AsyncEvaluationTopicsResource) -> None:
        self._evaluation_topics = evaluation_topics

        self.create = async_to_streamed_response_wrapper(
            evaluation_topics.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_topics.retrieve,
        )
