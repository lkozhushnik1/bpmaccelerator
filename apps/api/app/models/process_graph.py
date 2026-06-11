"""Process graph model — directed graph for rendering and editing."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class NodeType(str, Enum):
    start = "start"
    end = "end"
    task = "task"
    decision = "decision"
    approval = "approval"
    integration = "integration"
    notification = "notification"
    validation = "validation"


class EdgeType(str, Enum):
    sequence = "sequence"
    conditional = "conditional"
    exception = "exception"
    parallel = "parallel"


class NodePosition(BaseModel):
    x: float = 0.0
    y: float = 0.0


class GraphNode(BaseModel):
    id: str
    label: str
    description: Optional[str] = None
    node_type: NodeType = NodeType.task
    actor_ids: list[str] = Field(default_factory=list)
    system_refs: list[str] = Field(default_factory=list)
    is_automated: bool = False
    automation_candidate: bool = False
    position: NodePosition = Field(default_factory=NodePosition)
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    edge_type: EdgeType = EdgeType.sequence
    condition: Optional[str] = None


class Swimlane(BaseModel):
    id: str
    label: str
    node_ids: list[str] = Field(default_factory=list)


class ProcessGraph(BaseModel):
    process_id: str
    schema_version: str = "1.0.0"
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)
    swimlanes: list[Swimlane] = Field(default_factory=list)
