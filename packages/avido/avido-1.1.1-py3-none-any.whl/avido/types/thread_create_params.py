# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ThreadCreateParams"]


class ThreadCreateParams(TypedDict, total=False):
    application_id: Required[Annotated[str, PropertyInfo(alias="applicationId")]]
    """ID of the application this thread belongs to"""

    evaluation_id: Annotated[Optional[str], PropertyInfo(alias="evaluationId")]
    """Optional evaluation ID to link this thread to"""

    message: Optional[Dict[str, object]]
    """Optional initial message or payload"""

    metadata: Optional[Dict[str, object]]
    """Optional metadata for the thread"""
