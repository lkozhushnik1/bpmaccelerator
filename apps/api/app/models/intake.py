"""Process intake models — freeform and structured BYOP modes."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class IntakeMode(str, Enum):
    freeform = "freeform"
    structured = "structured"


class ProcessIntake(BaseModel):
    """Intake payload — accepts either freeform prompt or structured BYOP fields."""

    mode: IntakeMode = Field(..., description="Intake mode: freeform or structured.")
    prompt: Optional[str] = Field(
        None,
        min_length=10,
        description="Freeform process description (required when mode=freeform).",
    )
    industry: Optional[str] = Field(None, description="Industry or sector.")
    process_name: Optional[str] = Field(None, description="Short name for the process.")
    departments: list[str] = Field(default_factory=list, description="Departments involved.")
    overview: Optional[str] = Field(None, description="2–5 sentence process description.")
    key_steps: list[str] = Field(default_factory=list, description="Ordered list of major steps.")
    pain_points: list[str] = Field(default_factory=list, description="Current problems.")
    automation_goals: list[str] = Field(default_factory=list, description="Automation objectives.")
    systems: list[str] = Field(default_factory=list, description="Systems and tools involved.")
    approvals: list[str] = Field(default_factory=list, description="Approval steps and owners.")
    risks: list[str] = Field(default_factory=list, description="Known risks and exceptions.")
    constraints: list[str] = Field(default_factory=list, description="Constraints.")
    success_metrics: list[str] = Field(default_factory=list, description="KPIs and success criteria.")

    @model_validator(mode="after")
    def validate_mode_fields(self) -> "ProcessIntake":
        if self.mode == IntakeMode.freeform and not self.prompt:
            raise ValueError("prompt is required when mode is 'freeform'")
        if self.mode == IntakeMode.structured and not self.process_name:
            raise ValueError("process_name is required when mode is 'structured'")
        if self.mode == IntakeMode.structured and not self.overview:
            raise ValueError("overview is required when mode is 'structured'")
        return self

    model_config = {"json_schema_extra": {"example": {
        "mode": "structured",
        "industry": "Financial Services (Insurance)",
        "process_name": "Cloud Cost Anomaly Detection and Remediation",
        "departments": ["FinOps", "Cloud Platform Engineering"],
        "overview": "Identifies and resolves unexpected increases in cloud spend.",
        "key_steps": ["Detect anomaly", "Correlate signals", "Root cause analysis"],
        "automation_goals": ["Automated closed-loop detect-analyse-act-validate cycle"],
        "systems": ["AWS Cost Explorer", "Splunk", "ServiceNow"],
    }}}
