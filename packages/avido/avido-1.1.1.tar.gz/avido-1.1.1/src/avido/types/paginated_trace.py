# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["PaginatedTrace", "Data", "Pagination"]


class Data(BaseModel):
    id: str

    application_id: str = FieldInfo(alias="applicationId")
    """ID of the application this trace belongs to"""

    completion_tokens: Optional[float] = FieldInfo(alias="completionTokens", default=None)

    cost: Optional[float] = None

    created_at: str = FieldInfo(alias="createdAt")

    duration: Optional[float] = None

    ended_at: Optional[str] = FieldInfo(alias="endedAt", default=None)

    name: Optional[str] = None

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this trace"""

    prompt_tokens: Optional[float] = FieldInfo(alias="promptTokens", default=None)

    runtime: Optional[str] = None

    source: Optional[str] = None

    status: Optional[str] = None

    test_id: Optional[str] = FieldInfo(alias="testId", default=None)
    """Optional ID of the test this trace belongs to"""

    type: str

    error: Optional[object] = None

    input: Optional[object] = None

    metadata: Optional[object] = None

    output: Optional[object] = None

    params: Optional[object] = None


class Pagination(BaseModel):
    limit: float
    """Number of items per page"""

    skip: float
    """Number of items skipped"""

    total: float
    """Total number of items"""

    total_pages: float = FieldInfo(alias="totalPages")
    """Total number of pages"""


class PaginatedTrace(BaseModel):
    data: List[Data]

    pagination: Pagination
    """Pagination information in response"""
