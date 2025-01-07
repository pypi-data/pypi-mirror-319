# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import (
    protocol_parsing_list_params,
    protocol_parsing_error_params,
    protocol_parsing_success_params,
)
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
from ..types.protocol_parsing_list_response import ProtocolParsingListResponse

__all__ = ["ProtocolParsingsResource", "AsyncProtocolParsingsResource"]


class ProtocolParsingsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProtocolParsingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return ProtocolParsingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProtocolParsingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return ProtocolParsingsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolParsingListResponse:
        """
        Get Protocol Parsing Statuses

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/protocol-parsing",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    protocol_parsing_list_params.ProtocolParsingListParams,
                ),
            ),
            cast_to=ProtocolParsingListResponse,
        )

    def error(
        self,
        tenant: str,
        *,
        job_id: str,
        status_message: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Set Protocol Parsing Status Error

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        if not tenant:
            raise ValueError(f"Expected a non-empty value for `tenant` but received {tenant!r}")
        return self._post(
            f"/protocol-parsing/{job_id}/{tenant}/error",
            body=maybe_transform(
                {"status_message": status_message}, protocol_parsing_error_params.ProtocolParsingErrorParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def success(
        self,
        tenant: str,
        *,
        job_id: str,
        criteria_create: Iterable[protocol_parsing_success_params.CriteriaCreate],
        external_protocol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Update Protocol With Parsed Criteria And Set Success

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        if not tenant:
            raise ValueError(f"Expected a non-empty value for `tenant` but received {tenant!r}")
        return self._post(
            f"/protocol-parsing/{job_id}/{tenant}/success",
            body=maybe_transform(
                {
                    "criteria_create": criteria_create,
                    "external_protocol_id": external_protocol_id,
                },
                protocol_parsing_success_params.ProtocolParsingSuccessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncProtocolParsingsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProtocolParsingsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncProtocolParsingsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProtocolParsingsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AsyncProtocolParsingsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ProtocolParsingListResponse:
        """
        Get Protocol Parsing Statuses

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/protocol-parsing",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    protocol_parsing_list_params.ProtocolParsingListParams,
                ),
            ),
            cast_to=ProtocolParsingListResponse,
        )

    async def error(
        self,
        tenant: str,
        *,
        job_id: str,
        status_message: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Set Protocol Parsing Status Error

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        if not tenant:
            raise ValueError(f"Expected a non-empty value for `tenant` but received {tenant!r}")
        return await self._post(
            f"/protocol-parsing/{job_id}/{tenant}/error",
            body=await async_maybe_transform(
                {"status_message": status_message}, protocol_parsing_error_params.ProtocolParsingErrorParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def success(
        self,
        tenant: str,
        *,
        job_id: str,
        criteria_create: Iterable[protocol_parsing_success_params.CriteriaCreate],
        external_protocol_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Update Protocol With Parsed Criteria And Set Success

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        if not tenant:
            raise ValueError(f"Expected a non-empty value for `tenant` but received {tenant!r}")
        return await self._post(
            f"/protocol-parsing/{job_id}/{tenant}/success",
            body=await async_maybe_transform(
                {
                    "criteria_create": criteria_create,
                    "external_protocol_id": external_protocol_id,
                },
                protocol_parsing_success_params.ProtocolParsingSuccessParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class ProtocolParsingsResourceWithRawResponse:
    def __init__(self, protocol_parsings: ProtocolParsingsResource) -> None:
        self._protocol_parsings = protocol_parsings

        self.list = to_raw_response_wrapper(
            protocol_parsings.list,
        )
        self.error = to_raw_response_wrapper(
            protocol_parsings.error,
        )
        self.success = to_raw_response_wrapper(
            protocol_parsings.success,
        )


class AsyncProtocolParsingsResourceWithRawResponse:
    def __init__(self, protocol_parsings: AsyncProtocolParsingsResource) -> None:
        self._protocol_parsings = protocol_parsings

        self.list = async_to_raw_response_wrapper(
            protocol_parsings.list,
        )
        self.error = async_to_raw_response_wrapper(
            protocol_parsings.error,
        )
        self.success = async_to_raw_response_wrapper(
            protocol_parsings.success,
        )


class ProtocolParsingsResourceWithStreamingResponse:
    def __init__(self, protocol_parsings: ProtocolParsingsResource) -> None:
        self._protocol_parsings = protocol_parsings

        self.list = to_streamed_response_wrapper(
            protocol_parsings.list,
        )
        self.error = to_streamed_response_wrapper(
            protocol_parsings.error,
        )
        self.success = to_streamed_response_wrapper(
            protocol_parsings.success,
        )


class AsyncProtocolParsingsResourceWithStreamingResponse:
    def __init__(self, protocol_parsings: AsyncProtocolParsingsResource) -> None:
        self._protocol_parsings = protocol_parsings

        self.list = async_to_streamed_response_wrapper(
            protocol_parsings.list,
        )
        self.error = async_to_streamed_response_wrapper(
            protocol_parsings.error,
        )
        self.success = async_to_streamed_response_wrapper(
            protocol_parsings.success,
        )
