# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import date

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
from ...types.system import patient_create_params, patient_update_params
from ...types.shared.patient_read import PatientRead

__all__ = ["PatientsResource", "AsyncPatientsResource"]


class PatientsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PatientsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return PatientsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PatientsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return PatientsResourceWithStreamingResponse(self)

    def create(
        self,
        tenant_id: str,
        *,
        dob: Union[str, date, None],
        email: Optional[str],
        external_patient_id: str,
        family_name: str,
        given_name: str,
        site_id: int,
        do_not_call: Optional[bool] | NotGiven = NOT_GIVEN,
        middle_name: Optional[str] | NotGiven = NOT_GIVEN,
        phone: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRead:
        """
        Create Patient

        Args:
          tenant_id: The tenant ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_id:
            raise ValueError(f"Expected a non-empty value for `tenant_id` but received {tenant_id!r}")
        return self._post(
            f"/system/{tenant_id}/patients",
            body=maybe_transform(
                {
                    "dob": dob,
                    "email": email,
                    "external_patient_id": external_patient_id,
                    "family_name": family_name,
                    "given_name": given_name,
                    "site_id": site_id,
                    "do_not_call": do_not_call,
                    "middle_name": middle_name,
                    "phone": phone,
                },
                patient_create_params.PatientCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRead,
        )

    def update(
        self,
        patient_id: int,
        *,
        tenant_id: str,
        dob: Optional[str] | NotGiven = NOT_GIVEN,
        do_not_call: Optional[bool] | NotGiven = NOT_GIVEN,
        email: Optional[str] | NotGiven = NOT_GIVEN,
        external_patient_id: Optional[str] | NotGiven = NOT_GIVEN,
        family_name: Optional[str] | NotGiven = NOT_GIVEN,
        given_name: Optional[str] | NotGiven = NOT_GIVEN,
        middle_name: Optional[str] | NotGiven = NOT_GIVEN,
        phone: Optional[str] | NotGiven = NOT_GIVEN,
        site_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRead:
        """
        Patch Patient

        Args:
          tenant_id: The tenant ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_id:
            raise ValueError(f"Expected a non-empty value for `tenant_id` but received {tenant_id!r}")
        return self._patch(
            f"/system/{tenant_id}/patients/{patient_id}",
            body=maybe_transform(
                {
                    "dob": dob,
                    "do_not_call": do_not_call,
                    "email": email,
                    "external_patient_id": external_patient_id,
                    "family_name": family_name,
                    "given_name": given_name,
                    "middle_name": middle_name,
                    "phone": phone,
                    "site_id": site_id,
                },
                patient_update_params.PatientUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRead,
        )


class AsyncPatientsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPatientsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncPatientsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPatientsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TriallyAI/web-recruitment-sdk#with_streaming_response
        """
        return AsyncPatientsResourceWithStreamingResponse(self)

    async def create(
        self,
        tenant_id: str,
        *,
        dob: Union[str, date, None],
        email: Optional[str],
        external_patient_id: str,
        family_name: str,
        given_name: str,
        site_id: int,
        do_not_call: Optional[bool] | NotGiven = NOT_GIVEN,
        middle_name: Optional[str] | NotGiven = NOT_GIVEN,
        phone: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRead:
        """
        Create Patient

        Args:
          tenant_id: The tenant ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_id:
            raise ValueError(f"Expected a non-empty value for `tenant_id` but received {tenant_id!r}")
        return await self._post(
            f"/system/{tenant_id}/patients",
            body=await async_maybe_transform(
                {
                    "dob": dob,
                    "email": email,
                    "external_patient_id": external_patient_id,
                    "family_name": family_name,
                    "given_name": given_name,
                    "site_id": site_id,
                    "do_not_call": do_not_call,
                    "middle_name": middle_name,
                    "phone": phone,
                },
                patient_create_params.PatientCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRead,
        )

    async def update(
        self,
        patient_id: int,
        *,
        tenant_id: str,
        dob: Optional[str] | NotGiven = NOT_GIVEN,
        do_not_call: Optional[bool] | NotGiven = NOT_GIVEN,
        email: Optional[str] | NotGiven = NOT_GIVEN,
        external_patient_id: Optional[str] | NotGiven = NOT_GIVEN,
        family_name: Optional[str] | NotGiven = NOT_GIVEN,
        given_name: Optional[str] | NotGiven = NOT_GIVEN,
        middle_name: Optional[str] | NotGiven = NOT_GIVEN,
        phone: Optional[str] | NotGiven = NOT_GIVEN,
        site_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PatientRead:
        """
        Patch Patient

        Args:
          tenant_id: The tenant ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tenant_id:
            raise ValueError(f"Expected a non-empty value for `tenant_id` but received {tenant_id!r}")
        return await self._patch(
            f"/system/{tenant_id}/patients/{patient_id}",
            body=await async_maybe_transform(
                {
                    "dob": dob,
                    "do_not_call": do_not_call,
                    "email": email,
                    "external_patient_id": external_patient_id,
                    "family_name": family_name,
                    "given_name": given_name,
                    "middle_name": middle_name,
                    "phone": phone,
                    "site_id": site_id,
                },
                patient_update_params.PatientUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PatientRead,
        )


class PatientsResourceWithRawResponse:
    def __init__(self, patients: PatientsResource) -> None:
        self._patients = patients

        self.create = to_raw_response_wrapper(
            patients.create,
        )
        self.update = to_raw_response_wrapper(
            patients.update,
        )


class AsyncPatientsResourceWithRawResponse:
    def __init__(self, patients: AsyncPatientsResource) -> None:
        self._patients = patients

        self.create = async_to_raw_response_wrapper(
            patients.create,
        )
        self.update = async_to_raw_response_wrapper(
            patients.update,
        )


class PatientsResourceWithStreamingResponse:
    def __init__(self, patients: PatientsResource) -> None:
        self._patients = patients

        self.create = to_streamed_response_wrapper(
            patients.create,
        )
        self.update = to_streamed_response_wrapper(
            patients.update,
        )


class AsyncPatientsResourceWithStreamingResponse:
    def __init__(self, patients: AsyncPatientsResource) -> None:
        self._patients = patients

        self.create = async_to_streamed_response_wrapper(
            patients.create,
        )
        self.update = async_to_streamed_response_wrapper(
            patients.update,
        )
