"""Process normalizer — converts intake (freeform or structured) to NormalizedProcess."""

import re
from datetime import datetime, timezone

from app.models.intake import IntakeMode, ProcessIntake
from app.models.normalized_process import (
    Actor,
    Artifact,
    ArtifactType,
    Control,
    ControlType,
    KPI,
    NormalizedProcess,
    PainPoint,
    ProcessMetadata,
    ProcessOverview,
    RoleType,
    Step,
    StepType,
    System,
    SystemType,
)

_SYSTEM_TYPE_HINTS: dict[str, SystemType] = {
    "servicenow": SystemType.itsm,
    "jira": SystemType.itsm,
    "splunk": SystemType.observability,
    "new relic": SystemType.observability,
    "datadog": SystemType.observability,
    "aws cost": SystemType.cloud_cost,
    "azure cost": SystemType.cloud_cost,
    "databricks": SystemType.data_platform,
    "snowflake": SystemType.data_platform,
    "salesforce": SystemType.crm,
    "sap": SystemType.erp,
    "sharepoint": SystemType.document,
    "teams": SystemType.communication,
    "slack": SystemType.communication,
}


def _infer_system_type(name: str) -> SystemType:
    lower = name.lower()
    for keyword, stype in _SYSTEM_TYPE_HINTS.items():
        if keyword in lower:
            return stype
    return SystemType.other


def _slug(text: str, prefix: str) -> str:
    """Create a short ID slug from text."""
    clean = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:30]
    return f"{prefix}-{clean}"


def _infer_step_type(step_text: str) -> StepType:
    lower = step_text.lower()
    if any(w in lower for w in ("approve", "approval", "authoris", "authoriz")):
        return StepType.approval
    if any(w in lower for w in ("decide", "decision", "classify", "check", "validat")):
        return StepType.decision
    if any(w in lower for w in ("notify", "notif", "alert", "escalate")):
        return StepType.notification
    if any(w in lower for w in ("integrat", "sync", "route", "ticket", "create ticket")):
        return StepType.integration
    if any(w in lower for w in ("validate", "verify", "confirm", "test outcome")):
        return StepType.validation
    return StepType.task


def _is_automation_candidate(step_text: str) -> bool:
    lower = step_text.lower()
    manual_signals = ("approve", "review", "sign off", "manual", "human")
    return not any(w in lower for w in manual_signals)


def normalize(intake: ProcessIntake) -> NormalizedProcess:
    """Convert a ProcessIntake into a NormalizedProcess."""

    if intake.mode == IntakeMode.freeform:
        return _normalize_freeform(intake)
    return _normalize_structured(intake)


def _normalize_freeform(intake: ProcessIntake) -> NormalizedProcess:
    """Normalize a freeform prompt intake."""
    prompt = intake.prompt or ""
    process_name = intake.process_name or _extract_process_name(prompt)

    metadata = ProcessMetadata(
        name=process_name,
        industry=intake.industry,
        departments=intake.departments,
        created_at=datetime.now(timezone.utc),
    )

    overview = ProcessOverview(
        description=prompt[:500],
        objectives=["Automate and optimize the described business process"],
        triggers=["User-initiated process submission"],
        outcomes=["Structured process model, agent plan, and deployment artifacts"],
    )

    steps = _extract_steps_from_prompt(prompt)
    systems = _build_systems(intake.systems)
    actors = _build_default_actors(intake.departments)
    pain_points = _build_pain_points(intake.pain_points)
    kpis = _build_kpis(intake.success_metrics)

    return NormalizedProcess(
        metadata=metadata,
        overview=overview,
        actors=actors,
        steps=steps,
        systems=systems,
        pain_points=pain_points,
        automation_goals=intake.automation_goals,
        kpis=kpis,
    )


def _normalize_structured(intake: ProcessIntake) -> NormalizedProcess:
    """Normalize a structured BYOP intake."""
    process_name = intake.process_name or "Unnamed Process"

    metadata = ProcessMetadata(
        name=process_name,
        industry=intake.industry,
        departments=intake.departments,
        created_at=datetime.now(timezone.utc),
    )

    overview = ProcessOverview(
        description=intake.overview or "",
        objectives=intake.automation_goals[:3] if intake.automation_goals else [],
        triggers=[f"Process initiation for: {process_name}"],
        outcomes=[m for m in intake.success_metrics[:3]] if intake.success_metrics else [],
    )

    steps = _build_steps(intake.key_steps)
    systems = _build_systems(intake.systems)
    actors = _build_actors_from_departments(intake.departments, systems)
    pain_points = _build_pain_points(intake.pain_points)
    controls = _build_controls(intake.approvals, intake.risks, steps)
    artifacts = _build_artifacts(steps)
    kpis = _build_kpis(intake.success_metrics)

    return NormalizedProcess(
        metadata=metadata,
        overview=overview,
        actors=actors,
        steps=steps,
        systems=systems,
        artifacts=artifacts,
        controls=controls,
        pain_points=pain_points,
        automation_goals=intake.automation_goals,
        kpis=kpis,
    )


# ── helpers ───────────────────────────────────────────────────────────────────


def _extract_process_name(prompt: str) -> str:
    """Attempt to extract a short process name from a freeform prompt."""
    first_sentence = re.split(r"[.\n]", prompt)[0].strip()
    return first_sentence[:60] if first_sentence else "Business Process"


def _extract_steps_from_prompt(prompt: str) -> list[Step]:
    """Extract steps from a freeform prompt using heuristics."""
    lines = [l.strip() for l in prompt.splitlines() if l.strip()]
    step_lines: list[str] = []

    for line in lines:
        stripped = re.sub(r"^[\d]+[.)]\s*", "", line)
        stripped = re.sub(r"^[-•*]\s*", "", stripped)
        if len(stripped) > 5:
            step_lines.append(stripped)

    if not step_lines:
        step_lines = ["Process start", "Execute process", "Process end"]

    steps: list[Step] = []
    for i, text in enumerate(step_lines[:20], start=1):
        steps.append(Step(
            id=f"step-{i:02d}",
            name=text[:80],
            description=text,
            sequence=i,
            step_type=_infer_step_type(text),
            automation_candidate=_is_automation_candidate(text),
        ))
    return steps


def _build_steps(key_steps: list[str]) -> list[Step]:
    steps: list[Step] = []
    for i, text in enumerate(key_steps, start=1):
        steps.append(Step(
            id=f"step-{i:02d}",
            name=text[:80],
            description=text,
            sequence=i,
            step_type=_infer_step_type(text),
            automation_candidate=_is_automation_candidate(text),
        ))
    return steps


def _build_systems(system_names: list[str]) -> list[System]:
    systems: list[System] = []
    for name in system_names:
        systems.append(System(
            id=_slug(name, "sys"),
            name=name,
            system_type=_infer_system_type(name),
        ))
    return systems


def _build_default_actors(departments: list[str]) -> list[Actor]:
    actors: list[Actor] = []
    for dept in departments:
        actors.append(Actor(
            id=_slug(dept, "actor"),
            name=dept,
            role_type=RoleType.human,
        ))
    if not actors:
        actors.append(Actor(id="actor-team", name="Process Team", role_type=RoleType.human))
    return actors


def _build_actors_from_departments(departments: list[str], systems: list[System]) -> list[Actor]:
    actors = _build_default_actors(departments)
    # Add a system actor if there are any system integrations
    if systems:
        actors.append(Actor(
            id="actor-systems",
            name="Integrated Systems",
            role_type=RoleType.system,
            systems=[s.name for s in systems],
        ))
    return actors


def _build_pain_points(pain_point_texts: list[str]) -> list[PainPoint]:
    return [
        PainPoint(id=f"pp-{i:02d}", description=text)
        for i, text in enumerate(pain_point_texts, start=1)
    ]


def _build_controls(
    approvals: list[str], risks: list[str], steps: list[Step]
) -> list[Control]:
    controls: list[Control] = []
    for i, text in enumerate(approvals, start=1):
        # Associate approval controls with approval-type steps
        related = [s.id for s in steps if s.step_type == StepType.approval]
        controls.append(Control(
            id=f"ctrl-{i:02d}",
            name=f"Approval: {text[:50]}",
            control_type=ControlType.approval,
            related_step_ids=related[:2],
            description=text,
        ))
    for i, text in enumerate(risks, start=len(approvals) + 1):
        controls.append(Control(
            id=f"ctrl-{i:02d}",
            name=f"Risk: {text[:50]}",
            control_type=ControlType.risk,
            description=text,
        ))
    return controls


def _build_artifacts(steps: list[Step]) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for i, step in enumerate(steps, start=1):
        if step.step_type in (StepType.approval, StepType.integration, StepType.validation):
            artifacts.append(Artifact(
                id=f"art-{i:02d}",
                name=f"{step.name} Output",
                artifact_type=ArtifactType.output,
                owner_step_id=step.id,
            ))
    return artifacts


def _build_kpis(success_metrics: list[str]) -> list[KPI]:
    return [
        KPI(id=f"kpi-{i:02d}", name=metric[:80])
        for i, metric in enumerate(success_metrics, start=1)
    ]
