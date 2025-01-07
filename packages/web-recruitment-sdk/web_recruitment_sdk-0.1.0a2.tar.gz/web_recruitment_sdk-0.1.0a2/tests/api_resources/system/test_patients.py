# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from web_recruitment_sdk import WebRecruitmentSDK, AsyncWebRecruitmentSDK
from web_recruitment_sdk._utils import parse_date
from web_recruitment_sdk.types.shared import PatientRead

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPatients:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: WebRecruitmentSDK) -> None:
        patient = client.system.patients.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: WebRecruitmentSDK) -> None:
        patient = client.system.patients.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
            do_not_call=True,
            middle_name="middleName",
            phone="phone",
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: WebRecruitmentSDK) -> None:
        response = client.system.patients.with_raw_response.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = response.parse()
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: WebRecruitmentSDK) -> None:
        with client.system.patients.with_streaming_response.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = response.parse()
            assert_matches_type(PatientRead, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: WebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant_id` but received ''"):
            client.system.patients.with_raw_response.create(
                tenant_id="",
                dob=parse_date("2019-12-27"),
                email="email",
                external_patient_id="externalPatientId",
                family_name="familyName",
                given_name="givenName",
                site_id=0,
            )

    @parametrize
    def test_method_update(self, client: WebRecruitmentSDK) -> None:
        patient = client.system.patients.update(
            patient_id=0,
            tenant_id="tenant_id",
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: WebRecruitmentSDK) -> None:
        patient = client.system.patients.update(
            patient_id=0,
            tenant_id="tenant_id",
            dob="dob",
            do_not_call=True,
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            middle_name="middleName",
            phone="phone",
            site_id="siteId",
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: WebRecruitmentSDK) -> None:
        response = client.system.patients.with_raw_response.update(
            patient_id=0,
            tenant_id="tenant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = response.parse()
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: WebRecruitmentSDK) -> None:
        with client.system.patients.with_streaming_response.update(
            patient_id=0,
            tenant_id="tenant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = response.parse()
            assert_matches_type(PatientRead, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: WebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant_id` but received ''"):
            client.system.patients.with_raw_response.update(
                patient_id=0,
                tenant_id="",
            )


class TestAsyncPatients:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        patient = await async_client.system.patients.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncWebRecruitmentSDK) -> None:
        patient = await async_client.system.patients.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
            do_not_call=True,
            middle_name="middleName",
            phone="phone",
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.system.patients.with_raw_response.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = await response.parse()
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.system.patients.with_streaming_response.create(
            tenant_id="tenant_id",
            dob=parse_date("2019-12-27"),
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            site_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = await response.parse()
            assert_matches_type(PatientRead, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncWebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant_id` but received ''"):
            await async_client.system.patients.with_raw_response.create(
                tenant_id="",
                dob=parse_date("2019-12-27"),
                email="email",
                external_patient_id="externalPatientId",
                family_name="familyName",
                given_name="givenName",
                site_id=0,
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        patient = await async_client.system.patients.update(
            patient_id=0,
            tenant_id="tenant_id",
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncWebRecruitmentSDK) -> None:
        patient = await async_client.system.patients.update(
            patient_id=0,
            tenant_id="tenant_id",
            dob="dob",
            do_not_call=True,
            email="email",
            external_patient_id="externalPatientId",
            family_name="familyName",
            given_name="givenName",
            middle_name="middleName",
            phone="phone",
            site_id="siteId",
        )
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        response = await async_client.system.patients.with_raw_response.update(
            patient_id=0,
            tenant_id="tenant_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        patient = await response.parse()
        assert_matches_type(PatientRead, patient, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        async with async_client.system.patients.with_streaming_response.update(
            patient_id=0,
            tenant_id="tenant_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            patient = await response.parse()
            assert_matches_type(PatientRead, patient, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncWebRecruitmentSDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tenant_id` but received ''"):
            await async_client.system.patients.with_raw_response.update(
                patient_id=0,
                tenant_id="",
            )
