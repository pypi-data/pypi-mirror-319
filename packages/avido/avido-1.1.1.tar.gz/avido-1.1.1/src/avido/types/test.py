# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Test", "Data", "DataEvaluationCase", "DataEvaluationCaseApplication", "DataEvaluationCaseTopic", "DataRun"]


class DataEvaluationCaseApplication(BaseModel):
    id: str
    """Unique identifier of the application"""

    context: str
    """Context/instructions for the application"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the application was created"""

    description: str
    """Description of the application"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the application was last modified"""

    monitoring_enabled: bool = FieldInfo(alias="monitoringEnabled")
    """Whether monitoring is enabled for the application"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this application"""

    slug: str
    """URL-friendly slug for the application"""

    title: str
    """Title of the application"""

    type: Literal["CHATBOT", "AGENT"]
    """Type of the application"""


class DataEvaluationCaseTopic(BaseModel):
    id: str
    """Unique identifier of the evaluation topic"""

    benchmark: Optional[float] = None
    """Optional benchmark score for this topic"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the topic was created"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the topic was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this topic"""

    title: str
    """Title of the evaluation topic"""


class DataEvaluationCase(BaseModel):
    id: str
    """Unique identifier of the evaluation case"""

    application: DataEvaluationCaseApplication
    """Application configuration and metadata"""

    application_id: str = FieldInfo(alias="applicationId")
    """ID of the application this case belongs to"""

    benchmark: Optional[float] = None
    """Optional benchmark score for this case"""

    cot_approach: Optional[str] = FieldInfo(alias="cotApproach", default=None)
    """Chain of thought approach for evaluation"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the case was created"""

    evaluation_criteria: str = FieldInfo(alias="evaluationCriteria")
    """Criteria for evaluating the task"""

    factual_correctness: bool = FieldInfo(alias="factualCorrectness")
    """Whether factual correctness should be evaluated"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the case was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this case"""

    style_requirements: bool = FieldInfo(alias="styleRequirements")
    """Whether style requirements should be evaluated"""

    task: str
    """The task to be evaluated"""

    topic: DataEvaluationCaseTopic
    """Details about an evaluation topic"""

    topic_id: str = FieldInfo(alias="topicId")
    """ID of the evaluation topic"""


class DataRun(BaseModel):
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


class Data(BaseModel):
    id: str
    """Unique identifier of the test"""

    analysis: Optional[str] = None
    """Analysis of the test results"""

    clarity_score: Optional[float] = FieldInfo(alias="clarityScore", default=None)
    """Clarity score of the response"""

    coherence_score: Optional[float] = FieldInfo(alias="coherenceScore", default=None)
    """Coherence score of the response"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the test was created"""

    engagingness_score: Optional[float] = FieldInfo(alias="engagingnessScore", default=None)
    """Engagingness score of the response"""

    evaluation_case: DataEvaluationCase = FieldInfo(alias="evaluationCase")
    """Evaluation case configuration and metadata"""

    evaluation_case_id: str = FieldInfo(alias="evaluationCaseId")
    """ID of the evaluation case this test belongs to"""

    factual_consistency_score: Optional[float] = FieldInfo(alias="factualConsistencyScore", default=None)
    """Factual consistency score of the response"""

    llm_response: Optional[str] = FieldInfo(alias="llmResponse", default=None)
    """The LLM's response to the test prompt"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the test was last modified"""

    naturalness_score: Optional[float] = FieldInfo(alias="naturalnessScore", default=None)
    """Naturalness score of the response"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this test"""

    overall_score: Optional[float] = FieldInfo(alias="overallScore", default=None)
    """Overall score of the test"""

    relevance_score: Optional[float] = FieldInfo(alias="relevanceScore", default=None)
    """Relevance score of the response"""

    runs: List[DataRun]

    style_requirement_score: Optional[float] = FieldInfo(alias="styleRequirementScore", default=None)
    """Style requirement score of the response"""

    user_prompt: str = FieldInfo(alias="userPrompt")
    """The user prompt for the test"""


class Test(BaseModel):
    __test__ = False
    data: Data
    """Complete test with related evaluation case and runs information"""
