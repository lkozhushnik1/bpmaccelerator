"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.intake import IntakeMode, ProcessIntake


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def structured_intake() -> ProcessIntake:
    return ProcessIntake(
        mode=IntakeMode.structured,
        industry="Financial Services (Insurance)",
        process_name="Cloud Cost Anomaly Detection and Remediation",
        departments=["FinOps", "Cloud Platform Engineering", "Application Teams"],
        overview=(
            "Identifies and resolves unexpected increases in cloud spend across hybrid environments."
        ),
        key_steps=[
            "Detect cost anomaly",
            "Correlate infrastructure changes",
            "Root cause analysis",
            "Generate remediation actions",
            "Request approvals",
            "Execute approved actions",
            "Validate outcomes",
        ],
        pain_points=[
            "Fragmented tooling",
            "Slow manual analysis",
            "Approval bottlenecks",
        ],
        automation_goals=[
            "Automated closed-loop detect-analyse-act-validate cycle",
        ],
        systems=["AWS Cost Explorer", "Splunk", "New Relic", "ServiceNow"],
        approvals=["FinOps approval for actions > $1000/month"],
        success_metrics=["MTTD < 15 minutes", "MTTR < 4 hours"],
    )


@pytest.fixture
def freeform_intake() -> ProcessIntake:
    return ProcessIntake(
        mode=IntakeMode.freeform,
        prompt=(
            "Our employee onboarding process starts when HR receives a new hire request. "
            "The recruiter reviews the candidate, HR creates the employee record, IT provisions accounts, "
            "and the manager schedules onboarding sessions. Finally, compliance completes required training."
        ),
    )
