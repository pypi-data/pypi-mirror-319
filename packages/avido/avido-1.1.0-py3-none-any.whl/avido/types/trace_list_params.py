# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["TraceListParams"]


class TraceListParams(TypedDict, total=False):
    application_slug: Annotated[str, PropertyInfo(alias="applicationSlug")]
    """Filter by application slug"""

    end_date: Annotated[Union[str, datetime], PropertyInfo(alias="endDate", format="iso8601")]
    """Filter traces created before this date"""

    limit: int
    """Number of items per page"""

    order_by: Annotated[str, PropertyInfo(alias="orderBy")]
    """Field to order by"""

    order_dir: Annotated[Literal["asc", "desc"], PropertyInfo(alias="orderDir")]
    """Order direction"""

    skip: int
    """Number of items to skip"""

    start_date: Annotated[Union[str, datetime], PropertyInfo(alias="startDate", format="iso8601")]
    """Filter traces created after this date"""

    test_id: Annotated[str, PropertyInfo(alias="testId")]
    """Filter by test ID"""

    type: str
    """Filter by trace type"""
