# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ThreadCreateResponse", "Data"]


class Data(BaseModel):
    id: str
    """Unique identifier of the thread"""

    application_id: str = FieldInfo(alias="applicationId")
    """ID of the application this thread belongs to"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the thread was created"""

    evaluation_id: Optional[str] = FieldInfo(alias="evaluationId", default=None)
    """Optional evaluation ID this thread is linked to"""

    message: Optional[Dict[str, object]] = None
    """Optional initial message or payload"""

    metadata: Optional[Dict[str, object]] = None
    """Optional metadata for the thread"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the thread was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this thread"""


class ThreadCreateResponse(BaseModel):
    data: Data
    """Thread configuration and metadata"""
