"""Deployment router — manifest generation endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.models.normalized_process import NormalizedProcess
from app.models.agent_plan import AgentPlan
from app.models.deployment_manifest import DeploymentManifest
from app.services.agent_planner import build_agent_plan
from app.services.deployment_composer import compose_manifest

router = APIRouter()


class ManifestRequest(BaseModel):
    process: NormalizedProcess
    agent_plan: AgentPlan | None = None
    environment: str = "dev"


@router.post("/manifest", response_model=DeploymentManifest)
async def generate_manifest(request: ManifestRequest) -> DeploymentManifest:
    """
    Generate an Azure deployment manifest from a NormalizedProcess and optional AgentPlan.
    If no agent_plan is provided, one is derived automatically.
    """
    plan = request.agent_plan or build_agent_plan(request.process)
    return compose_manifest(request.process, plan, request.environment)
