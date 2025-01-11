# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import webhook_validate_params
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
from ..types.webhook_validate_response import WebhookValidateResponse

__all__ = ["WebhooksResource", "AsyncWebhooksResource"]


class WebhooksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return WebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return WebhooksResourceWithStreamingResponse(self)

    def validate(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookValidateResponse:
        """
        Checks headers and the request body against the configured webhook secret.
        Returns `{ valid: true }` if the signature is valid.

        Args:
          body: The raw JSON payload sent by the external webhook. Arbitrary fields are allowed;
              signature verification is used for security.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/validate-webhook",
            body=maybe_transform(body, webhook_validate_params.WebhookValidateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookValidateResponse,
        )


class AsyncWebhooksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Avido-AI/avido-py#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Avido-AI/avido-py#with_streaming_response
        """
        return AsyncWebhooksResourceWithStreamingResponse(self)

    async def validate(
        self,
        *,
        body: object,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookValidateResponse:
        """
        Checks headers and the request body against the configured webhook secret.
        Returns `{ valid: true }` if the signature is valid.

        Args:
          body: The raw JSON payload sent by the external webhook. Arbitrary fields are allowed;
              signature verification is used for security.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/validate-webhook",
            body=await async_maybe_transform(body, webhook_validate_params.WebhookValidateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookValidateResponse,
        )


class WebhooksResourceWithRawResponse:
    def __init__(self, webhooks: WebhooksResource) -> None:
        self._webhooks = webhooks

        self.validate = to_raw_response_wrapper(
            webhooks.validate,
        )


class AsyncWebhooksResourceWithRawResponse:
    def __init__(self, webhooks: AsyncWebhooksResource) -> None:
        self._webhooks = webhooks

        self.validate = async_to_raw_response_wrapper(
            webhooks.validate,
        )


class WebhooksResourceWithStreamingResponse:
    def __init__(self, webhooks: WebhooksResource) -> None:
        self._webhooks = webhooks

        self.validate = to_streamed_response_wrapper(
            webhooks.validate,
        )


class AsyncWebhooksResourceWithStreamingResponse:
    def __init__(self, webhooks: AsyncWebhooksResource) -> None:
        self._webhooks = webhooks

        self.validate = async_to_streamed_response_wrapper(
            webhooks.validate,
        )
