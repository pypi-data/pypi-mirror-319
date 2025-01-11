# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["ThreadList", "ThreadListItem"]


class ThreadListItem(BaseModel):
    application_id: str
    """Application ID (UUID)."""

    org_id: str
    """Organization ID (UUID)."""

    thread_id: str
    """Unique Thread ID (UUID)."""

    timestamp: str
    """ISO-8601 datetime when the thread was triggered/created."""

    type: Literal["thread"]
    """Type of the event (always `thread` for threads)."""

    input: Optional[Dict[str, object]] = None
    """JSON describing the initial input that started the thread."""

    metadata: Optional[Dict[str, object]] = None
    """Arbitrary metadata for this thread (e.g., userId, source, etc.)."""

    test_id: Optional[str] = None
    """Optional test/evaluation ID for the thread."""


ThreadList: TypeAlias = List[ThreadListItem]
