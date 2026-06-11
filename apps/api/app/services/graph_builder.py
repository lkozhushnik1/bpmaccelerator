"""Graph builder — converts a NormalizedProcess into a ProcessGraph."""

import math

from app.models.normalized_process import NormalizedProcess, RoleType, StepType
from app.models.process_graph import (
    EdgeType,
    GraphEdge,
    GraphNode,
    NodePosition,
    NodeType,
    ProcessGraph,
    Swimlane,
)

_STEP_TYPE_TO_NODE_TYPE: dict[StepType, NodeType] = {
    StepType.task: NodeType.task,
    StepType.decision: NodeType.decision,
    StepType.approval: NodeType.approval,
    StepType.notification: NodeType.notification,
    StepType.integration: NodeType.integration,
    StepType.validation: NodeType.validation,
    StepType.start: NodeType.start,
    StepType.end: NodeType.end,
}

_HORIZONTAL_GAP = 200
_VERTICAL_GAP = 120


def build_graph(process: NormalizedProcess) -> ProcessGraph:
    """Convert a NormalizedProcess to a ProcessGraph."""
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []

    # Start node
    start_node = GraphNode(
        id="node-start",
        label="Start",
        node_type=NodeType.start,
        position=NodePosition(x=0, y=0),
    )
    nodes.append(start_node)

    previous_id = "node-start"

    for step in sorted(process.steps, key=lambda s: s.sequence):
        node_id = f"node-{step.id}"
        node_type = _STEP_TYPE_TO_NODE_TYPE.get(step.step_type, NodeType.task)

        x = step.sequence * _HORIZONTAL_GAP
        y = _compute_y(step.id, process.actors, step.actor_ids)

        node = GraphNode(
            id=node_id,
            label=step.name,
            description=step.description,
            node_type=node_type,
            actor_ids=step.actor_ids,
            system_refs=step.system_refs,
            is_automated=step.is_automated,
            automation_candidate=step.automation_candidate,
            position=NodePosition(x=x, y=y),
        )
        nodes.append(node)

        edge = GraphEdge(
            id=f"edge-{previous_id}-{node_id}",
            source=previous_id,
            target=node_id,
            edge_type=EdgeType.sequence,
        )
        edges.append(edge)
        previous_id = node_id

    # End node
    end_x = (len(process.steps) + 1) * _HORIZONTAL_GAP
    end_node = GraphNode(
        id="node-end",
        label="End",
        node_type=NodeType.end,
        position=NodePosition(x=end_x, y=0),
    )
    nodes.append(end_node)
    edges.append(GraphEdge(
        id=f"edge-{previous_id}-node-end",
        source=previous_id,
        target="node-end",
        edge_type=EdgeType.sequence,
    ))

    # Decision edges from process.decisions
    for decision in process.decisions:
        for label, target_step_id in decision.branches.items():
            source_node_id = f"node-step-{decision.id.replace('dec-', 'step-')}"
            # try to find the matching step node
            target_node_id = f"node-{target_step_id}"
            if any(n.id == source_node_id for n in nodes) and any(n.id == target_node_id for n in nodes):
                edges.append(GraphEdge(
                    id=f"edge-dec-{decision.id}-{label}",
                    source=source_node_id,
                    target=target_node_id,
                    label=label,
                    edge_type=EdgeType.conditional,
                    condition=decision.condition,
                ))

    # Swimlanes — one per unique actor
    swimlanes = _build_swimlanes(process, nodes)

    return ProcessGraph(
        process_id=process.id,
        nodes=nodes,
        edges=edges,
        swimlanes=swimlanes,
    )


def _compute_y(step_id: str, actors: list, actor_ids: list[str]) -> float:
    """Assign a vertical position based on the first actor's index."""
    if not actor_ids or not actors:
        return 0.0
    actor_id = actor_ids[0]
    for i, actor in enumerate(actors):
        if actor.id == actor_id:
            return i * _VERTICAL_GAP
    return 0.0


def _build_swimlanes(process: NormalizedProcess, nodes: list[GraphNode]) -> list[Swimlane]:
    """Build swimlanes grouping nodes by actor."""
    lane_map: dict[str, list[str]] = {}

    for actor in process.actors:
        lane_map[actor.id] = []

    for node in nodes:
        if not node.actor_ids:
            lane_map.setdefault("unassigned", []).append(node.id)
        else:
            for actor_id in node.actor_ids:
                lane_map.setdefault(actor_id, []).append(node.id)

    actor_name_map = {a.id: a.name for a in process.actors}

    swimlanes: list[Swimlane] = []
    for actor_id, node_ids in lane_map.items():
        if node_ids:
            swimlanes.append(Swimlane(
                id=f"lane-{actor_id}",
                label=actor_name_map.get(actor_id, actor_id),
                node_ids=node_ids,
            ))
    return swimlanes
