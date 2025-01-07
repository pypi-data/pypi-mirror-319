# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SiteUpdateParams"]


class SiteUpdateParams(TypedDict, total=False):
    tenant_id: Required[str]
    """The tenant ID"""

    name: Required[str]
