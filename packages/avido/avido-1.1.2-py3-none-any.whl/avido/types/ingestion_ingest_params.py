# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "IngestionIngestParams",
    "Event",
    "EventLlmEvent",
    "EventLlmEventError",
    "EventLlmEventTokensUsage",
    "EventToolEvent",
    "EventToolEventError",
    "EventToolEventTokensUsage",
    "EventThreadEvent",
    "EventThreadEventError",
    "EventThreadEventTokensUsage",
    "EventRetrieverEvent",
    "EventRetrieverEventError",
    "EventRetrieverEventTokensUsage",
    "EventLogEvent",
    "EventLogEventError",
    "EventLogEventTokensUsage",
]


class IngestionIngestParams(TypedDict, total=False):
    events: Required[Iterable[Event]]
    """
    An array of typed events (LLM usage, tool calls, threads, retriever queries, or
    logs).
    """


class EventLlmEventError(TypedDict, total=False):
    message: Required[str]
    """A short human-readable error message."""

    stack: Optional[str]
    """Optional stack trace or error details."""


class EventLlmEventTokensUsage(TypedDict, total=False):
    completion: Required[float]
    """Number of completion tokens used."""

    prompt: Required[float]
    """Number of prompt tokens used."""


class EventLlmEvent(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 timestamp for when the event occurred.

    Example: '2025-01-05T12:34:56.789Z'.
    """

    type: Required[Literal["llm"]]

    application_id: Annotated[Optional[str], PropertyInfo(alias="applicationId")]
    """UUID referencing your Avido application."""

    error: EventLlmEventError
    """Information about an error that occurred during an event."""

    evaluation_id: Annotated[Optional[str], PropertyInfo(alias="evaluationId")]
    """An optional evaluation/test ID (string)."""

    event: Optional[str]
    """A custom or sub-type label for the event (e.g. 'start', 'end')."""

    input: Optional[object]
    """
    Arbitrary JSON representing the input for this event (prompt, tool input, etc.).
    """

    message: Optional[object]
    """For chat events, could contain { role, content }. For others, it may be unused."""

    metadata: Optional[object]
    """Optional arbitrary metadata object, key-value pairs relevant to the event."""

    output: Optional[object]
    """
    Arbitrary JSON representing the output of this event (LLM output, tool result,
    etc.).
    """

    parent_run_id: Annotated[Optional[str], PropertyInfo(alias="parentRunId")]
    """UUID of the parent run, if this is a child event."""

    run_id: Annotated[Optional[str], PropertyInfo(alias="runId")]
    """Unique identifier for this run (UUID)."""

    tokens_usage: Annotated[EventLlmEventTokensUsage, PropertyInfo(alias="tokensUsage")]
    """Tracks how many tokens were used in a prompt/completion."""


class EventToolEventError(TypedDict, total=False):
    message: Required[str]
    """A short human-readable error message."""

    stack: Optional[str]
    """Optional stack trace or error details."""


class EventToolEventTokensUsage(TypedDict, total=False):
    completion: Required[float]
    """Number of completion tokens used."""

    prompt: Required[float]
    """Number of prompt tokens used."""


class EventToolEvent(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 timestamp for when the event occurred.

    Example: '2025-01-05T12:34:56.789Z'.
    """

    type: Required[Literal["tool"]]

    application_id: Annotated[Optional[str], PropertyInfo(alias="applicationId")]
    """UUID referencing your Avido application."""

    error: EventToolEventError
    """Information about an error that occurred during an event."""

    evaluation_id: Annotated[Optional[str], PropertyInfo(alias="evaluationId")]
    """An optional evaluation/test ID (string)."""

    event: Optional[str]
    """A custom or sub-type label for the event (e.g. 'start', 'end')."""

    input: Optional[object]
    """
    Arbitrary JSON representing the input for this event (prompt, tool input, etc.).
    """

    message: Optional[object]
    """For chat events, could contain { role, content }. For others, it may be unused."""

    metadata: Optional[object]
    """Optional arbitrary metadata object, key-value pairs relevant to the event."""

    output: Optional[object]
    """
    Arbitrary JSON representing the output of this event (LLM output, tool result,
    etc.).
    """

    parent_run_id: Annotated[Optional[str], PropertyInfo(alias="parentRunId")]
    """UUID of the parent run, if this is a child event."""

    run_id: Annotated[Optional[str], PropertyInfo(alias="runId")]
    """Unique identifier for this run (UUID)."""

    tokens_usage: Annotated[EventToolEventTokensUsage, PropertyInfo(alias="tokensUsage")]
    """Tracks how many tokens were used in a prompt/completion."""

    tool_call_input: Annotated[Optional[object], PropertyInfo(alias="toolCallInput")]
    """Arbitrary JSON representing the input provided to the tool."""

    tool_call_name: Annotated[Optional[str], PropertyInfo(alias="toolCallName")]
    """Name of the tool being called."""

    tool_call_output: Annotated[Optional[object], PropertyInfo(alias="toolCallOutput")]
    """Arbitrary JSON with the tool's output."""


class EventThreadEventError(TypedDict, total=False):
    message: Required[str]
    """A short human-readable error message."""

    stack: Optional[str]
    """Optional stack trace or error details."""


class EventThreadEventTokensUsage(TypedDict, total=False):
    completion: Required[float]
    """Number of completion tokens used."""

    prompt: Required[float]
    """Number of prompt tokens used."""


class EventThreadEvent(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 timestamp for when the event occurred.

    Example: '2025-01-05T12:34:56.789Z'.
    """

    type: Required[Literal["thread"]]

    application_id: Annotated[Optional[str], PropertyInfo(alias="applicationId")]
    """UUID referencing your Avido application."""

    error: EventThreadEventError
    """Information about an error that occurred during an event."""

    evaluation_id: Annotated[Optional[str], PropertyInfo(alias="evaluationId")]
    """An optional evaluation/test ID (string)."""

    event: Optional[str]
    """A custom or sub-type label for the event (e.g. 'start', 'end')."""

    input: Optional[object]
    """
    Arbitrary JSON representing the input for this event (prompt, tool input, etc.).
    """

    message: Optional[object]
    """For chat events, could contain { role, content }. For others, it may be unused."""

    metadata: Optional[object]
    """Optional arbitrary metadata object, key-value pairs relevant to the event."""

    output: Optional[object]
    """
    Arbitrary JSON representing the output of this event (LLM output, tool result,
    etc.).
    """

    parent_run_id: Annotated[Optional[str], PropertyInfo(alias="parentRunId")]
    """UUID of the parent run, if this is a child event."""

    run_id: Annotated[Optional[str], PropertyInfo(alias="runId")]
    """Unique identifier for this run (UUID)."""

    tokens_usage: Annotated[EventThreadEventTokensUsage, PropertyInfo(alias="tokensUsage")]
    """Tracks how many tokens were used in a prompt/completion."""


class EventRetrieverEventError(TypedDict, total=False):
    message: Required[str]
    """A short human-readable error message."""

    stack: Optional[str]
    """Optional stack trace or error details."""


class EventRetrieverEventTokensUsage(TypedDict, total=False):
    completion: Required[float]
    """Number of completion tokens used."""

    prompt: Required[float]
    """Number of prompt tokens used."""


class EventRetrieverEvent(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 timestamp for when the event occurred.

    Example: '2025-01-05T12:34:56.789Z'.
    """

    type: Required[Literal["retriever"]]

    application_id: Annotated[Optional[str], PropertyInfo(alias="applicationId")]
    """UUID referencing your Avido application."""

    error: EventRetrieverEventError
    """Information about an error that occurred during an event."""

    evaluation_id: Annotated[Optional[str], PropertyInfo(alias="evaluationId")]
    """An optional evaluation/test ID (string)."""

    event: Optional[str]
    """A custom or sub-type label for the event (e.g. 'start', 'end')."""

    input: Optional[object]
    """
    Arbitrary JSON representing the input for this event (prompt, tool input, etc.).
    """

    message: Optional[object]
    """For chat events, could contain { role, content }. For others, it may be unused."""

    metadata: Optional[object]
    """Optional arbitrary metadata object, key-value pairs relevant to the event."""

    output: Optional[object]
    """
    Arbitrary JSON representing the output of this event (LLM output, tool result,
    etc.).
    """

    parent_run_id: Annotated[Optional[str], PropertyInfo(alias="parentRunId")]
    """UUID of the parent run, if this is a child event."""

    retriever_query: Annotated[Optional[str], PropertyInfo(alias="retrieverQuery")]
    """RAG query used to retrieve data, if any."""

    retriever_result: Annotated[Optional[object], PropertyInfo(alias="retrieverResult")]
    """Arbitrary JSON object containing doc chunks or data retrieved."""

    run_id: Annotated[Optional[str], PropertyInfo(alias="runId")]
    """Unique identifier for this run (UUID)."""

    tokens_usage: Annotated[EventRetrieverEventTokensUsage, PropertyInfo(alias="tokensUsage")]
    """Tracks how many tokens were used in a prompt/completion."""


class EventLogEventError(TypedDict, total=False):
    message: Required[str]
    """A short human-readable error message."""

    stack: Optional[str]
    """Optional stack trace or error details."""


class EventLogEventTokensUsage(TypedDict, total=False):
    completion: Required[float]
    """Number of completion tokens used."""

    prompt: Required[float]
    """Number of prompt tokens used."""


class EventLogEvent(TypedDict, total=False):
    timestamp: Required[str]
    """ISO-8601 timestamp for when the event occurred.

    Example: '2025-01-05T12:34:56.789Z'.
    """

    type: Required[Literal["log"]]

    application_id: Annotated[Optional[str], PropertyInfo(alias="applicationId")]
    """UUID referencing your Avido application."""

    error: EventLogEventError
    """Information about an error that occurred during an event."""

    evaluation_id: Annotated[Optional[str], PropertyInfo(alias="evaluationId")]
    """An optional evaluation/test ID (string)."""

    event: Optional[str]
    """A custom or sub-type label for the event (e.g. 'start', 'end')."""

    input: Optional[object]
    """
    Arbitrary JSON representing the input for this event (prompt, tool input, etc.).
    """

    message: Optional[object]
    """For chat events, could contain { role, content }. For others, it may be unused."""

    metadata: Optional[object]
    """Optional arbitrary metadata object, key-value pairs relevant to the event."""

    output: Optional[object]
    """
    Arbitrary JSON representing the output of this event (LLM output, tool result,
    etc.).
    """

    parent_run_id: Annotated[Optional[str], PropertyInfo(alias="parentRunId")]
    """UUID of the parent run, if this is a child event."""

    run_id: Annotated[Optional[str], PropertyInfo(alias="runId")]
    """Unique identifier for this run (UUID)."""

    tokens_usage: Annotated[EventLogEventTokensUsage, PropertyInfo(alias="tokensUsage")]
    """Tracks how many tokens were used in a prompt/completion."""


Event: TypeAlias = Union[EventLlmEvent, EventToolEvent, EventThreadEvent, EventRetrieverEvent, EventLogEvent]
