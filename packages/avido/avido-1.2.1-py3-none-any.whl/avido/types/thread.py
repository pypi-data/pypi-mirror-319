# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "Thread",
    "Data",
    "DataChildTrace",
    "DataChildTraceLlmTrace",
    "DataChildTraceToolTrace",
    "DataChildTraceRetrieverTrace",
    "DataChildTraceLogTrace",
]


class DataChildTraceLlmTrace(BaseModel):
    application_id: str
    """Application ID (UUID)."""

    api_model_id: str = FieldInfo(alias="model_id")
    """Model ID or name used for the LLM call."""

    org_id: str
    """Organization ID (UUID)."""

    thread_id: str
    """UUID referencing the parent thread's ID."""

    timestamp: str
    """ISO-8601 datetime for when the trace event occurred."""

    trace_id: str
    """UUID for the trace."""

    type: Literal["llm"]

    completion_tokens: Optional[float] = None
    """Number of completion tokens used by the LLM."""

    event: Optional[str] = None
    """Event label (e.g., 'start', 'end'). Specific to LLM traces."""

    input: Optional[Dict[str, object]] = None
    """JSON input for this LLM trace event (e.g., the prompt)."""

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event."""

    output: Optional[Dict[str, object]] = None
    """JSON output for this LLM trace event (e.g., the completion)."""

    params: Optional[Dict[str, object]] = None
    """Arbitrary LLM params (temperature, top_p, etc.)."""

    prompt_tokens: Optional[float] = None
    """Number of prompt tokens used by the LLM."""


class DataChildTraceToolTrace(BaseModel):
    application_id: str
    """Application ID (UUID)."""

    org_id: str
    """Organization ID (UUID)."""

    thread_id: str
    """UUID referencing the parent thread's ID."""

    timestamp: str
    """ISO-8601 datetime for when the trace event occurred."""

    trace_id: str
    """UUID for the trace."""

    type: Literal["tool"]

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event."""

    tool_input: Optional[Dict[str, object]] = None
    """JSON input for the tool call."""

    tool_output: Optional[Dict[str, object]] = None
    """JSON output from the tool call."""


class DataChildTraceRetrieverTrace(BaseModel):
    application_id: str
    """Application ID (UUID)."""

    org_id: str
    """Organization ID (UUID)."""

    thread_id: str
    """UUID referencing the parent thread's ID."""

    timestamp: str
    """ISO-8601 datetime for when the trace event occurred."""

    trace_id: str
    """UUID for the trace."""

    type: Literal["retriever"]

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event."""

    retriever_query: Optional[str] = None
    """Query used for retrieval-augmented generation."""

    retriever_result: Optional[Dict[str, object]] = None
    """Retrieved data chunks, if any."""


class DataChildTraceLogTrace(BaseModel):
    application_id: str
    """Application ID (UUID)."""

    org_id: str
    """Organization ID (UUID)."""

    thread_id: str
    """UUID referencing the parent thread's ID."""

    timestamp: str
    """ISO-8601 datetime for when the trace event occurred."""

    trace_id: str
    """UUID for the trace."""

    type: Literal["log"]

    content: Optional[str] = None
    """The actual log message for this trace."""

    metadata: Optional[Dict[str, object]] = None
    """Extra metadata about this trace event."""


DataChildTrace: TypeAlias = Union[
    DataChildTraceLlmTrace, DataChildTraceToolTrace, DataChildTraceRetrieverTrace, DataChildTraceLogTrace
]


class Data(BaseModel):
    application_id: str
    """Application ID (UUID)."""

    child_traces: List[DataChildTrace]
    """Array of traces associated with the thread."""

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


class Thread(BaseModel):
    data: Data
