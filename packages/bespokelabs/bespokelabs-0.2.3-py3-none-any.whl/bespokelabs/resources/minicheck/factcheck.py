# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.minicheck import factcheck_create_params
from ...types.minicheck.factcheck_create_response import FactcheckCreateResponse

__all__ = ["FactcheckResource", "AsyncFactcheckResource"]


class FactcheckResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FactcheckResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bespokelabsai/bespokelabs-python#accessing-raw-response-data-eg-headers
        """
        return FactcheckResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FactcheckResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bespokelabsai/bespokelabs-python#with_streaming_response
        """
        return FactcheckResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        claim: str,
        context: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FactcheckCreateResponse:
        """
        Factcheck Single Context

        Args:
          claim: The claim to be fact-checked.

          context: The context to fact-check against.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v0/minicheck/factcheck",
            body=maybe_transform(
                {
                    "claim": claim,
                    "context": context,
                },
                factcheck_create_params.FactcheckCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FactcheckCreateResponse,
        )


class AsyncFactcheckResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFactcheckResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/bespokelabsai/bespokelabs-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFactcheckResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFactcheckResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/bespokelabsai/bespokelabs-python#with_streaming_response
        """
        return AsyncFactcheckResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        claim: str,
        context: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FactcheckCreateResponse:
        """
        Factcheck Single Context

        Args:
          claim: The claim to be fact-checked.

          context: The context to fact-check against.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v0/minicheck/factcheck",
            body=await async_maybe_transform(
                {
                    "claim": claim,
                    "context": context,
                },
                factcheck_create_params.FactcheckCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FactcheckCreateResponse,
        )


class FactcheckResourceWithRawResponse:
    def __init__(self, factcheck: FactcheckResource) -> None:
        self._factcheck = factcheck

        self.create = to_raw_response_wrapper(
            factcheck.create,
        )


class AsyncFactcheckResourceWithRawResponse:
    def __init__(self, factcheck: AsyncFactcheckResource) -> None:
        self._factcheck = factcheck

        self.create = async_to_raw_response_wrapper(
            factcheck.create,
        )


class FactcheckResourceWithStreamingResponse:
    def __init__(self, factcheck: FactcheckResource) -> None:
        self._factcheck = factcheck

        self.create = to_streamed_response_wrapper(
            factcheck.create,
        )


class AsyncFactcheckResourceWithStreamingResponse:
    def __init__(self, factcheck: AsyncFactcheckResource) -> None:
        self._factcheck = factcheck

        self.create = async_to_streamed_response_wrapper(
            factcheck.create,
        )
