"""Deployment manifest model — Azure resource deployment specification."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Environment(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"


class ContainerAppIngress(BaseModel):
    external: bool = True
    target_port: int = 8000


class ContainerApp(BaseModel):
    name: str
    image: str
    cpu: float = 0.5
    memory: str = "1Gi"
    env_vars: dict[str, str] = Field(default_factory=dict)
    ingress: Optional[ContainerAppIngress] = None


class StorageAccount(BaseModel):
    name: str
    sku: str = "Standard_LRS"
    containers: list[str] = Field(default_factory=list)


class KeyVault(BaseModel):
    name: str
    sku: str = "standard"


class LogAnalytics(BaseModel):
    name: str
    retention_days: int = 30


class ApplicationInsights(BaseModel):
    name: str


class ManagedIdentity(BaseModel):
    name: str


class ModelDeployment(BaseModel):
    name: str
    model: str
    capacity: int = 1


class AIFoundryWorkspace(BaseModel):
    workspace_name: str
    model_deployments: list[ModelDeployment] = Field(default_factory=list)


class Resources(BaseModel):
    container_apps: list[ContainerApp] = Field(default_factory=list)
    storage_account: Optional[StorageAccount] = None
    key_vault: Optional[KeyVault] = None
    log_analytics: Optional[LogAnalytics] = None
    application_insights: Optional[ApplicationInsights] = None
    managed_identity: Optional[ManagedIdentity] = None
    ai_foundry: Optional[AIFoundryWorkspace] = None


class DeploymentManifest(BaseModel):
    process_id: str
    schema_version: str = "1.0.0"
    environment: Environment = Environment.dev
    azure_region: str = "australiaeast"
    resource_group: Optional[str] = None
    resources: Resources = Field(default_factory=Resources)
    outputs: dict[str, str] = Field(default_factory=dict)
