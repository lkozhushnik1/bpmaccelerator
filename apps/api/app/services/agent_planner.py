"""Agent planner — derives an Azure AI Foundry agent plan from a NormalizedProcess."""

from app.models.agent_plan import (
    Agent,
    AgentPlan,
    AgentRole,
    AgentTool,
    DataFlow,
    HumanCheckpoint,
    OrchestrationPattern,
    ToolType,
)
from app.models.normalized_process import NormalizedProcess, StepType


def build_agent_plan(process: NormalizedProcess) -> AgentPlan:
    """Derive an agent plan from a normalized process."""
    agents: list[Agent] = []
    checkpoints: list[HumanCheckpoint] = []
    data_flows: list[DataFlow] = []

    # Planner agent — always present
    planner = Agent(
        id="agent-planner",
        name="Process Orchestration Planner",
        role=AgentRole.planner,
        description="Coordinates the end-to-end process automation workflow, routes tasks to specialist agents.",
        trigger="New process intake submission",
        inputs=["process_intake"],
        outputs=["orchestration_plan"],
        tools=[AgentTool(name="process_router", tool_type=ToolType.custom,
                          description="Routes process steps to appropriate specialist agents")],
        human_in_loop=False,
    )
    agents.append(planner)

    # Derive specialist agents from step types and automation candidates
    automation_steps = [s for s in process.steps if s.automation_candidate]
    approval_steps = [s for s in process.steps if s.step_type == StepType.approval]
    integration_steps = [s for s in process.steps if s.step_type == StepType.integration]
    validation_steps = [s for s in process.steps if s.step_type == StepType.validation]

    # Process Intake & Normalization agent
    if automation_steps:
        intake_agent = Agent(
            id="agent-intake",
            name="Process Intake Agent",
            role=AgentRole.specialist,
            description="Interprets and normalizes the business process description, extracts structured entities.",
            trigger="Triggered by planner after intake submission",
            inputs=["raw_process_input"],
            outputs=["normalized_process"],
            tools=[
                AgentTool(name="entity_extractor", tool_type=ToolType.document_processor,
                           description="Extracts process entities from freeform text"),
                AgentTool(name="schema_validator", tool_type=ToolType.custom,
                           description="Validates output against NormalizedProcess schema"),
            ],
            human_in_loop=False,
            related_step_ids=[s.id for s in automation_steps[:3]],
        )
        agents.append(intake_agent)
        data_flows.append(DataFlow(from_agent="agent-planner", to_agent="agent-intake", artifact="process_intake"))

    # Analysis / RCA agent — for data-heavy or integration steps
    if integration_steps or len(process.systems) > 2:
        analysis_agent = Agent(
            id="agent-analysis",
            name="Process Analysis Agent",
            role=AgentRole.specialist,
            description="Correlates data from multiple systems, performs root cause or pattern analysis.",
            trigger="Triggered by planner with correlated data sources",
            inputs=["system_data", "observability_data"],
            outputs=["analysis_report", "root_cause"],
            tools=[
                AgentTool(name="data_correlator", tool_type=ToolType.api_connector,
                           description="Connects to integrated systems to retrieve and correlate data"),
                AgentTool(name="semantic_search", tool_type=ToolType.search,
                           description="Semantic search across process knowledge base"),
                AgentTool(name="code_runner", tool_type=ToolType.code_interpreter,
                           description="Executes analytical queries and transformations"),
            ],
            human_in_loop=False,
            related_step_ids=[s.id for s in integration_steps[:5]],
            foundry_config=None,
        )
        agents.append(analysis_agent)
        data_flows.append(DataFlow(from_agent="agent-intake", to_agent="agent-analysis", artifact="normalized_process"))

    # Action recommendation agent
    if process.automation_goals:
        action_agent = Agent(
            id="agent-action",
            name="Action Recommendation Agent",
            role=AgentRole.specialist,
            description="Generates and ranks recommended actions based on analysis results and automation goals.",
            trigger="Triggered by analysis agent with analysis report",
            inputs=["analysis_report", "automation_goals"],
            outputs=["ranked_action_plan"],
            tools=[
                AgentTool(name="action_generator", tool_type=ToolType.custom,
                           description="Generates candidate remediation or optimisation actions"),
                AgentTool(name="impact_scorer", tool_type=ToolType.custom,
                           description="Scores actions by impact, effort, and risk"),
            ],
            human_in_loop=False,
        )
        agents.append(action_agent)
        if len(agents) >= 3:
            data_flows.append(DataFlow(from_agent="agent-analysis", to_agent="agent-action", artifact="analysis_report"))

    # Approval routing agent
    if approval_steps:
        approval_agent = Agent(
            id="agent-approval",
            name="Approval Routing Agent",
            role=AgentRole.specialist,
            description="Routes actions to appropriate approvers based on ownership, risk level, and thresholds.",
            trigger="Triggered by action recommendation agent with ranked action plan",
            inputs=["ranked_action_plan", "ownership_metadata"],
            outputs=["approval_requests", "itsm_tickets"],
            tools=[
                AgentTool(name="itsm_connector", tool_type=ToolType.api_connector,
                           description="Creates and updates ITSM tickets (e.g. ServiceNow)"),
                AgentTool(name="approval_gate", tool_type=ToolType.human_approval,
                           description="Requests human approval for high-impact actions"),
            ],
            human_in_loop=True,
            related_step_ids=[s.id for s in approval_steps],
        )
        agents.append(approval_agent)
        checkpoints.append(HumanCheckpoint(
            id="checkpoint-approval",
            name="Human Approval Gate",
            description="Human review and approval required before high-impact actions are executed.",
            after_agent_id="agent-approval",
        ))

    # Execution agent
    exec_agent = Agent(
        id="agent-execution",
        name="Action Execution Agent",
        role=AgentRole.specialist,
        description="Executes approved low-risk actions autonomously; escalates high-risk actions to human operators.",
        trigger="Triggered after approval checkpoint with approved action plan",
        inputs=["approved_actions"],
        outputs=["execution_results"],
        tools=[
            AgentTool(name="system_executor", tool_type=ToolType.api_connector,
                       description="Executes actions against target systems via APIs"),
        ],
        human_in_loop=False,
    )
    agents.append(exec_agent)

    # Validator agent
    if validation_steps:
        validator = Agent(
            id="agent-validator",
            name="Outcome Validation Agent",
            role=AgentRole.validator,
            description="Validates that executed actions achieved the expected outcomes and KPIs.",
            trigger="Triggered after execution agent with execution results",
            inputs=["execution_results", "expected_outcomes"],
            outputs=["validation_report"],
            tools=[
                AgentTool(name="outcome_checker", tool_type=ToolType.custom,
                           description="Checks actual vs expected outcomes against KPIs"),
            ],
            human_in_loop=False,
            related_step_ids=[s.id for s in validation_steps],
        )
        agents.append(validator)
        checkpoints.append(HumanCheckpoint(
            id="checkpoint-validation",
            name="Human Validation Review",
            description="Human review of validation report before closing process instance.",
            after_agent_id="agent-validator",
        ))

    return AgentPlan(
        process_id=process.id,
        orchestration_pattern=OrchestrationPattern.planner_specialists_validator,
        agents=agents,
        human_checkpoints=checkpoints,
        data_flow=data_flows,
    )
