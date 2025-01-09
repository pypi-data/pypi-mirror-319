# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["IngestionIngestResponse", "Result"]


class Result(BaseModel):
    success: bool
    """Whether the event was successfully ingested."""

    id: Optional[str] = None
    """Event ID assigned upon ingestion (if any)."""

    error: Optional[str] = None
    """Error message if ingestion failed."""


class IngestionIngestResponse(BaseModel):
    results: List[Result]
