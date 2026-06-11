"""Normalized process model — canonical intermediate representation."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class RoleType(str, Enum):
    human = "human"
    system = "system"
    agent = "agent"
    external = "external"


class StepType(str, Enum):
    task = "task"
    decision = "decision"
    approval = "approval"
    notification = "notification"
    integration = "integration"
    validation = "validation"
    start = "start"
    end = "end"


class ArtifactType(str, Enum):
    input = "input"
    output = "output"
    report = "report"
    ticket = "ticket"
    approval = "approval"
    notification = "notification"
    data = "data"


class ControlType(str, Enum):
    approval = "approval"
    compliance = "compliance"
    risk = "risk"
    audit = "audit"
    sla = "sla"
    threshold = "threshold"


class SystemType(str, Enum):
    itsm = "itsm"
    observability = "observability"
    cloud_cost = "cloud_cost"
    erp = "erp"
    crm = "crm"
    document = "document"
    communication = "communication"
    data_platform = "data_platform"
    other = "other"


class ProcessMetadata(BaseModel):
    name: str
    version: str = "1.0.0"
    industry: Optional[str] = None
    departments: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags: dict[str, str] = Field(default_factory=dict)


class ProcessOverview(BaseModel):
    description: str
    objectives: list[str] = Field(default_factory=list)
    triggers: list[str] = Field(default_factory=list)
    outcomes: list[str] = Field(default_factory=list)


class Actor(BaseModel):
    id: str
    name: str
    role_type: RoleType
    systems: list[str] = Field(default_factory=list)


class Step(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    sequence: int = Field(ge=1)
    actor_ids: list[str] = Field(default_factory=list)
    system_refs: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    step_type: StepType = StepType.task
    is_automated: bool = False
    automation_candidate: bool = False
    duration_minutes: Optional[float] = None


class Decision(BaseModel):
    id: str
    name: str
    condition: str
    branches: dict[str, str] = Field(default_factory=dict)


class Artifact(BaseModel):
    id: str
    name: str
    artifact_type: ArtifactType
    format: Optional[str] = None
    owner_step_id: Optional[str] = None


class Control(BaseModel):
    id: str
    name: str
    control_type: ControlType
    related_step_ids: list[str] = Field(default_factory=list)
    description: Optional[str] = None


class PainPoint(BaseModel):
    id: str
    description: str
    affected_steps: list[str] = Field(default_factory=list)


class System(BaseModel):
    id: str
    name: str
    system_type: SystemType = SystemType.other
    vendor: Optional[str] = None


class KPI(BaseModel):
    id: str
    name: str
    target: Optional[str] = None
    unit: Optional[str] = None


class NormalizedProcess(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    schema_version: str = "1.0.0"
    metadata: ProcessMetadata
    overview: ProcessOverview
    actors: list[Actor] = Field(default_factory=list)
    steps: list[Step] = Field(default_factory=list)
    decisions: list[Decision] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    controls: list[Control] = Field(default_factory=list)
    pain_points: list[PainPoint] = Field(default_factory=list)
    automation_goals: list[str] = Field(default_factory=list)
    systems: list[System] = Field(default_factory=list)
    kpis: list[KPI] = Field(default_factory=list)
