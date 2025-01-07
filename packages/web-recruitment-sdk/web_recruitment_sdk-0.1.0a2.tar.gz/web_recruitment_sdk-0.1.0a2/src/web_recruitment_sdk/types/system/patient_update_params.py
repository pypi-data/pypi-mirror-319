# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["PatientUpdateParams"]


class PatientUpdateParams(TypedDict, total=False):
    tenant_id: Required[str]
    """The tenant ID"""

    dob: Optional[str]

    do_not_call: Annotated[Optional[bool], PropertyInfo(alias="doNotCall")]

    email: Optional[str]

    external_patient_id: Annotated[Optional[str], PropertyInfo(alias="externalPatientId")]

    family_name: Annotated[Optional[str], PropertyInfo(alias="familyName")]

    given_name: Annotated[Optional[str], PropertyInfo(alias="givenName")]

    middle_name: Annotated[Optional[str], PropertyInfo(alias="middleName")]

    phone: Optional[str]

    site_id: Annotated[Optional[str], PropertyInfo(alias="siteId")]
