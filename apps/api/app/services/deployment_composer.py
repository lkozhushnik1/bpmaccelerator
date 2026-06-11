"""Deployment composer — generates an Azure deployment manifest from a process and agent plan."""

import re

from app.models.agent_plan import AgentPlan
from app.models.deployment_manifest import (
    AIFoundryWorkspace,
    ApplicationInsights,
    ContainerApp,
    ContainerAppIngress,
    DeploymentManifest,
    Environment,
    KeyVault,
    LogAnalytics,
    ManagedIdentity,
    ModelDeployment,
    Resources,
    StorageAccount,
)
from app.models.normalized_process import NormalizedProcess


def _safe_name(text: str, max_len: int = 24) -> str:
    """Create a safe Azure resource name from text."""
    clean = re.sub(r"[^a-z0-9]", "", text.lower())
    return clean[:max_len]


def compose_manifest(
    process: NormalizedProcess,
    agent_plan: AgentPlan,
    environment: str = "dev",
) -> DeploymentManifest:
    """Compose an Azure deployment manifest from process and agent plan."""
    env = Environment(environment) if environment in Environment.__members__ else Environment.dev

    base_name = _safe_name(process.metadata.name)
    rg_name = f"rg-bpmacc-{base_name}-{env.value}"

    has_foundry_agents = len(agent_plan.agents) > 0

    # Container Apps
    web_app = ContainerApp(
        name=f"ca-web-{base_name}",
        image="bpmaccelerator/web:latest",
        cpu=0.5,
        memory="1Gi",
        env_vars={
            "NEXT_PUBLIC_API_URL": f"https://ca-api-{base_name}.azurecontainerapps.io",
        },
        ingress=ContainerAppIngress(external=True, target_port=3000),
    )

    api_app = ContainerApp(
        name=f"ca-api-{base_name}",
        image="bpmaccelerator/api:latest",
        cpu=0.5,
        memory="1Gi",
        env_vars={
            "LOG_LEVEL": "INFO",
            "KEY_VAULT_NAME": f"kv-bpmacc-{base_name}",
        },
        ingress=ContainerAppIngress(external=True, target_port=8000),
    )

    storage = StorageAccount(
        name=f"stbpmacc{base_name}",
        sku="Standard_LRS",
        containers=["process-artifacts", "agent-outputs", "deployment-manifests"],
    )

    kv = KeyVault(name=f"kv-bpmacc-{base_name}")

    log_analytics = LogAnalytics(
        name=f"law-bpmacc-{base_name}",
        retention_days=30 if env == Environment.dev else 90,
    )

    app_insights = ApplicationInsights(name=f"appi-bpmacc-{base_name}")

    managed_identity = ManagedIdentity(name=f"id-bpmacc-{base_name}")

    ai_foundry: AIFoundryWorkspace | None = None
    if has_foundry_agents:
        ai_foundry = AIFoundryWorkspace(
            workspace_name=f"aif-bpmacc-{base_name}",
            model_deployments=[
                ModelDeployment(name="gpt-4o", model="gpt-4o", capacity=10),
                ModelDeployment(name="text-embedding-ada-002", model="text-embedding-ada-002", capacity=10),
            ],
        )

    resources = Resources(
        container_apps=[web_app, api_app],
        storage_account=storage,
        key_vault=kv,
        log_analytics=log_analytics,
        application_insights=app_insights,
        managed_identity=managed_identity,
        ai_foundry=ai_foundry,
    )

    outputs = {
        "webAppUrl": f"https://{web_app.name}.azurecontainerapps.io",
        "apiUrl": f"https://{api_app.name}.azurecontainerapps.io",
        "resourceGroup": rg_name,
    }

    return DeploymentManifest(
        process_id=process.id,
        environment=env,
        azure_region="australiaeast",
        resource_group=rg_name,
        resources=resources,
        outputs=outputs,
    )
