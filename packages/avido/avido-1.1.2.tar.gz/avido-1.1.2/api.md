# Ingestion

Types:

```python
from avido.types import IngestionIngestResponse
```

Methods:

- <code title="post /v0/ingest">client.ingestion.<a href="./src/avido/resources/ingestion.py">ingest</a>(\*\*<a href="src/avido/types/ingestion_ingest_params.py">params</a>) -> <a href="./src/avido/types/ingestion_ingest_response.py">IngestionIngestResponse</a></code>

# Threads

Types:

```python
from avido.types import ThreadCreateResponse
```

Methods:

- <code title="post /v0/threads">client.threads.<a href="./src/avido/resources/threads.py">create</a>(\*\*<a href="src/avido/types/thread_create_params.py">params</a>) -> <a href="./src/avido/types/thread_create_response.py">ThreadCreateResponse</a></code>

# Webhook

Types:

```python
from avido.types import WebhookValidateResponse
```

Methods:

- <code title="post /v0/validate-webhook">client.webhook.<a href="./src/avido/resources/webhook.py">validate</a>(\*\*<a href="src/avido/types/webhook_validate_params.py">params</a>) -> <a href="./src/avido/types/webhook_validate_response.py">WebhookValidateResponse</a></code>

# Evaluations

Types:

```python
from avido.types import EvaluationCase, PaginatedEvaluationCase, EvaluationListResponse
```

Methods:

- <code title="post /v0/evaluations">client.evaluations.<a href="./src/avido/resources/evaluations.py">create</a>(\*\*<a href="src/avido/types/evaluation_create_params.py">params</a>) -> <a href="./src/avido/types/evaluation_case.py">EvaluationCase</a></code>
- <code title="get /v0/evaluations/{id}">client.evaluations.<a href="./src/avido/resources/evaluations.py">retrieve</a>(id) -> <a href="./src/avido/types/evaluation_case.py">EvaluationCase</a></code>
- <code title="get /v0/evaluations">client.evaluations.<a href="./src/avido/resources/evaluations.py">list</a>(\*\*<a href="src/avido/types/evaluation_list_params.py">params</a>) -> <a href="./src/avido/types/evaluation_list_response.py">SyncOffsetPagination[EvaluationListResponse]</a></code>

# Applications

Types:

```python
from avido.types import Application, PaginatedApplication, ApplicationListResponse
```

Methods:

- <code title="post /v0/applications">client.applications.<a href="./src/avido/resources/applications.py">create</a>(\*\*<a href="src/avido/types/application_create_params.py">params</a>) -> <a href="./src/avido/types/application.py">Application</a></code>
- <code title="get /v0/applications/{id}">client.applications.<a href="./src/avido/resources/applications.py">retrieve</a>(id) -> <a href="./src/avido/types/application.py">Application</a></code>
- <code title="get /v0/applications">client.applications.<a href="./src/avido/resources/applications.py">list</a>(\*\*<a href="src/avido/types/application_list_params.py">params</a>) -> <a href="./src/avido/types/application_list_response.py">SyncOffsetPagination[ApplicationListResponse]</a></code>

# EvaluationTopics

Types:

```python
from avido.types import EvaluationTopic, PaginatedEvaluationTopic, EvaluationTopicListResponse
```

Methods:

- <code title="post /v0/topics">client.evaluation_topics.<a href="./src/avido/resources/evaluation_topics.py">create</a>(\*\*<a href="src/avido/types/evaluation_topic_create_params.py">params</a>) -> <a href="./src/avido/types/evaluation_topic.py">EvaluationTopic</a></code>
- <code title="get /v0/topics/{id}">client.evaluation_topics.<a href="./src/avido/resources/evaluation_topics.py">retrieve</a>(id) -> <a href="./src/avido/types/evaluation_topic.py">EvaluationTopic</a></code>
- <code title="get /v0/topics">client.evaluation_topics.<a href="./src/avido/resources/evaluation_topics.py">list</a>(\*\*<a href="src/avido/types/evaluation_topic_list_params.py">params</a>) -> <a href="./src/avido/types/evaluation_topic_list_response.py">SyncOffsetPagination[EvaluationTopicListResponse]</a></code>

# Tests

Types:

```python
from avido.types import PaginatedTest, Test, TestListResponse
```

Methods:

- <code title="get /v0/tests/{id}">client.tests.<a href="./src/avido/resources/tests.py">retrieve</a>(id) -> <a href="./src/avido/types/test.py">Test</a></code>
- <code title="get /v0/tests">client.tests.<a href="./src/avido/resources/tests.py">list</a>(\*\*<a href="src/avido/types/test_list_params.py">params</a>) -> <a href="./src/avido/types/test_list_response.py">SyncOffsetPagination[TestListResponse]</a></code>
- <code title="post /v0/tests/run">client.tests.<a href="./src/avido/resources/tests.py">run</a>(\*\*<a href="src/avido/types/test_run_params.py">params</a>) -> <a href="./src/avido/types/test.py">Test</a></code>

# Traces

Types:

```python
from avido.types import PaginatedTrace, Trace, TraceListResponse
```

Methods:

- <code title="get /v0/traces/{id}">client.traces.<a href="./src/avido/resources/traces.py">retrieve</a>(id) -> <a href="./src/avido/types/trace.py">Trace</a></code>
- <code title="get /v0/traces">client.traces.<a href="./src/avido/resources/traces.py">list</a>(\*\*<a href="src/avido/types/trace_list_params.py">params</a>) -> <a href="./src/avido/types/trace_list_response.py">SyncOffsetPagination[TraceListResponse]</a></code>
