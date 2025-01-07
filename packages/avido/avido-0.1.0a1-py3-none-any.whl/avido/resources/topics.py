# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import topic_list_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncOffsetPagination, AsyncOffsetPagination
from .._base_client import AsyncPaginator, make_request_options
from ..types.topic_list_response import TopicListResponse

__all__ = ["TopicsResource", "AsyncTopicsResource"]


class TopicsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return TopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return TopicsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        order_by: str | NotGiven = NOT_GIVEN,
        order_dir: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncOffsetPagination[TopicListResponse]:
        """
        Retrieves a paginated list of evaluation topics with optional filtering.

        Args:
          limit: Number of items per page

          order_by: Field to order by

          order_dir: Order direction

          skip: Number of items to skip

          title: Filter by topic title (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v0/topics",
            page=SyncOffsetPagination[TopicListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "order_by": order_by,
                        "order_dir": order_dir,
                        "skip": skip,
                        "title": title,
                    },
                    topic_list_params.TopicListParams,
                ),
            ),
            model=TopicListResponse,
        )


class AsyncTopicsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopicsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncTopicsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopicsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncTopicsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        order_by: str | NotGiven = NOT_GIVEN,
        order_dir: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        skip: int | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[TopicListResponse, AsyncOffsetPagination[TopicListResponse]]:
        """
        Retrieves a paginated list of evaluation topics with optional filtering.

        Args:
          limit: Number of items per page

          order_by: Field to order by

          order_dir: Order direction

          skip: Number of items to skip

          title: Filter by topic title (case-insensitive)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v0/topics",
            page=AsyncOffsetPagination[TopicListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "order_by": order_by,
                        "order_dir": order_dir,
                        "skip": skip,
                        "title": title,
                    },
                    topic_list_params.TopicListParams,
                ),
            ),
            model=TopicListResponse,
        )


class TopicsResourceWithRawResponse:
    def __init__(self, topics: TopicsResource) -> None:
        self._topics = topics

        self.list = to_raw_response_wrapper(
            topics.list,
        )


class AsyncTopicsResourceWithRawResponse:
    def __init__(self, topics: AsyncTopicsResource) -> None:
        self._topics = topics

        self.list = async_to_raw_response_wrapper(
            topics.list,
        )


class TopicsResourceWithStreamingResponse:
    def __init__(self, topics: TopicsResource) -> None:
        self._topics = topics

        self.list = to_streamed_response_wrapper(
            topics.list,
        )


class AsyncTopicsResourceWithStreamingResponse:
    def __init__(self, topics: AsyncTopicsResource) -> None:
        self._topics = topics

        self.list = async_to_streamed_response_wrapper(
            topics.list,
        )
