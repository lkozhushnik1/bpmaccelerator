"""Process routers — normalize, graph, and pipeline endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.models.intake import ProcessIntake
from app.models.normalized_process import NormalizedProcess
from app.models.process_graph import ProcessGraph
from app.models.agent_plan import AgentPlan
from app.models.deployment_manifest import DeploymentManifest
from app.services.normalizer import normalize
from app.services.graph_builder import build_graph
from app.services.agent_planner import build_agent_plan
from app.services.deployment_composer import compose_manifest

router = APIRouter()


class PipelineResult(BaseModel):
    normalized_process: NormalizedProcess
    process_graph: ProcessGraph
    agent_plan: AgentPlan
    deployment_manifest: DeploymentManifest


@router.post("/normalize", response_model=NormalizedProcess)
async def normalize_process(intake: ProcessIntake) -> NormalizedProcess:
    """
    Normalize a process intake (freeform or structured) into a canonical NormalizedProcess.
    """
    return normalize(intake)


@router.post("/graph", response_model=ProcessGraph)
async def build_process_graph(process: NormalizedProcess) -> ProcessGraph:
    """
    Generate a process graph from a NormalizedProcess.
    """
    return build_graph(process)


@router.post("/pipeline", response_model=PipelineResult)
async def run_pipeline(intake: ProcessIntake) -> PipelineResult:
    """
    Run the full transformation pipeline:
    intake → normalized process → graph → agent plan → deployment manifest.
    """
    process = normalize(intake)
    graph = build_graph(process)
    plan = build_agent_plan(process)
    manifest = compose_manifest(process, plan)
    return PipelineResult(
        normalized_process=process,
        process_graph=graph,
        agent_plan=plan,
        deployment_manifest=manifest,
    )
