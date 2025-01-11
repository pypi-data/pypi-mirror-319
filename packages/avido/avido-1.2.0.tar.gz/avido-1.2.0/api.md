# Webhooks

Types:

```python
from avido.types import WebhookValidateResponse
```

Methods:

- <code title="post /v0/validate-webhook">client.webhooks.<a href="./src/avido/resources/webhooks.py">validate</a>(\*\*<a href="src/avido/types/webhook_validate_params.py">params</a>) -> <a href="./src/avido/types/webhook_validate_response.py">WebhookValidateResponse</a></code>

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

# Topics

Types:

```python
from avido.types import EvaluationTopic, PaginatedEvaluationTopic, TopicListResponse
```

Methods:

- <code title="post /v0/topics">client.topics.<a href="./src/avido/resources/topics.py">create</a>(\*\*<a href="src/avido/types/topic_create_params.py">params</a>) -> <a href="./src/avido/types/evaluation_topic.py">EvaluationTopic</a></code>
- <code title="get /v0/topics/{id}">client.topics.<a href="./src/avido/resources/topics.py">retrieve</a>(id) -> <a href="./src/avido/types/evaluation_topic.py">EvaluationTopic</a></code>
- <code title="get /v0/topics">client.topics.<a href="./src/avido/resources/topics.py">list</a>(\*\*<a href="src/avido/types/topic_list_params.py">params</a>) -> <a href="./src/avido/types/topic_list_response.py">SyncOffsetPagination[TopicListResponse]</a></code>

# Tests

Types:

```python
from avido.types import PaginatedTest, Test, TestListResponse
```

Methods:

- <code title="get /v0/tests/{id}">client.tests.<a href="./src/avido/resources/tests.py">retrieve</a>(id) -> <a href="./src/avido/types/test.py">Test</a></code>
- <code title="get /v0/tests">client.tests.<a href="./src/avido/resources/tests.py">list</a>(\*\*<a href="src/avido/types/test_list_params.py">params</a>) -> <a href="./src/avido/types/test_list_response.py">SyncOffsetPagination[TestListResponse]</a></code>
- <code title="post /v0/tests/run">client.tests.<a href="./src/avido/resources/tests.py">run</a>(\*\*<a href="src/avido/types/test_run_params.py">params</a>) -> <a href="./src/avido/types/test.py">Test</a></code>

# Ingest

Types:

```python
from avido.types import IngestCreateResponse
```

Methods:

- <code title="post /v0/ingest">client.ingest.<a href="./src/avido/resources/ingest.py">create</a>(\*\*<a href="src/avido/types/ingest_create_params.py">params</a>) -> <a href="./src/avido/types/ingest_create_response.py">IngestCreateResponse</a></code>

# Threads

Types:

```python
from avido.types import Thread, ThreadList
```

Methods:

- <code title="get /v0/threads/{id}">client.threads.<a href="./src/avido/resources/threads.py">retrieve</a>(id) -> <a href="./src/avido/types/thread.py">Thread</a></code>
- <code title="get /v0/threads">client.threads.<a href="./src/avido/resources/threads.py">list</a>(\*\*<a href="src/avido/types/thread_list_params.py">params</a>) -> <a href="./src/avido/types/thread_list.py">ThreadList</a></code>
