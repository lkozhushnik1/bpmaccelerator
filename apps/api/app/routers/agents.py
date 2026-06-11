"""Agents router — agent plan endpoint."""

from fastapi import APIRouter

from app.models.normalized_process import NormalizedProcess
from app.models.agent_plan import AgentPlan
from app.services.agent_planner import build_agent_plan

router = APIRouter()


@router.post("/plan", response_model=AgentPlan)
async def create_agent_plan(process: NormalizedProcess) -> AgentPlan:
    """
    Generate an Azure AI Foundry agent plan from a NormalizedProcess.
    """
    return build_agent_plan(process)
