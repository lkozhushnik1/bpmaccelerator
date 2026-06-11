"""Agent plan model — Azure AI Foundry multi-agent orchestration design."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class OrchestrationPattern(str, Enum):
    planner_specialists_validator = "planner_specialists_validator"
    sequential = "sequential"
    parallel = "parallel"
    hierarchical = "hierarchical"


class AgentRole(str, Enum):
    planner = "planner"
    specialist = "specialist"
    validator = "validator"
    human_proxy = "human_proxy"


class ToolType(str, Enum):
    api_connector = "api_connector"
    document_processor = "document_processor"
    search = "search"
    code_interpreter = "code_interpreter"
    custom = "custom"
    human_approval = "human_approval"


class AgentTool(BaseModel):
    name: str
    tool_type: ToolType
    description: Optional[str] = None
    config: dict[str, Any] = Field(default_factory=dict)


class FoundryConfig(BaseModel):
    model_deployment: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class Agent(BaseModel):
    id: str
    name: str
    role: AgentRole
    description: Optional[str] = None
    trigger: str
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    tools: list[AgentTool] = Field(default_factory=list)
    human_in_loop: bool = False
    related_step_ids: list[str] = Field(default_factory=list)
    foundry_config: Optional[FoundryConfig] = None


class HumanCheckpoint(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    after_agent_id: str


class DataFlow(BaseModel):
    from_agent: str
    to_agent: str
    artifact: str


class AgentPlan(BaseModel):
    process_id: str
    schema_version: str = "1.0.0"
    orchestration_pattern: OrchestrationPattern = (
        OrchestrationPattern.planner_specialists_validator
    )
    agents: list[Agent] = Field(default_factory=list)
    human_checkpoints: list[HumanCheckpoint] = Field(default_factory=list)
    data_flow: list[DataFlow] = Field(default_factory=list)
