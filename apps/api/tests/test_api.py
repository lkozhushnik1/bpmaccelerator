"""Tests for the API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestNormalizeEndpoint:
    def test_normalize_structured(self, client: TestClient, structured_intake) -> None:
        response = client.post("/api/process/normalize", json=structured_intake.model_dump())
        assert response.status_code == 200
        data = response.json()
        assert data["metadata"]["name"] == structured_intake.process_name
        assert len(data["steps"]) == len(structured_intake.key_steps)

    def test_normalize_freeform(self, client: TestClient, freeform_intake) -> None:
        response = client.post("/api/process/normalize", json=freeform_intake.model_dump())
        assert response.status_code == 200
        data = response.json()
        assert "steps" in data
        assert len(data["steps"]) > 0

    def test_normalize_returns_id(self, client: TestClient, structured_intake) -> None:
        response = client.post("/api/process/normalize", json=structured_intake.model_dump())
        assert response.status_code == 200
        data = response.json()
        assert "id" in data and data["id"]

    def test_normalize_invalid_freeform_no_prompt(self, client: TestClient) -> None:
        response = client.post("/api/process/normalize", json={"mode": "freeform"})
        assert response.status_code == 422

    def test_normalize_invalid_structured_no_name(self, client: TestClient) -> None:
        response = client.post(
            "/api/process/normalize",
            json={"mode": "structured", "overview": "Some overview"},
        )
        assert response.status_code == 422


class TestGraphEndpoint:
    def test_build_graph_from_normalized_process(
        self, client: TestClient, structured_intake
    ) -> None:
        # First normalize
        norm_resp = client.post("/api/process/normalize", json=structured_intake.model_dump())
        assert norm_resp.status_code == 200
        normalized = norm_resp.json()

        # Then build graph
        graph_resp = client.post("/api/process/graph", json=normalized)
        assert graph_resp.status_code == 200
        graph = graph_resp.json()
        assert "nodes" in graph
        assert "edges" in graph
        assert len(graph["nodes"]) > 0
        assert len(graph["edges"]) > 0

    def test_graph_has_start_and_end_nodes(
        self, client: TestClient, structured_intake
    ) -> None:
        norm_resp = client.post("/api/process/normalize", json=structured_intake.model_dump())
        normalized = norm_resp.json()

        graph_resp = client.post("/api/process/graph", json=normalized)
        graph = graph_resp.json()

        node_types = [n["node_type"] for n in graph["nodes"]]
        assert "start" in node_types
        assert "end" in node_types


class TestAgentPlanEndpoint:
    def test_build_agent_plan(self, client: TestClient, structured_intake) -> None:
        norm_resp = client.post("/api/process/normalize", json=structured_intake.model_dump())
        normalized = norm_resp.json()

        plan_resp = client.post("/api/agents/plan", json=normalized)
        assert plan_resp.status_code == 200
        plan = plan_resp.json()
        assert "agents" in plan
        assert len(plan["agents"]) > 0
        assert "orchestration_pattern" in plan

    def test_agent_plan_has_planner(self, client: TestClient, structured_intake) -> None:
        norm_resp = client.post("/api/process/normalize", json=structured_intake.model_dump())
        plan_resp = client.post("/api/agents/plan", json=norm_resp.json())
        plan = plan_resp.json()
        roles = [a["role"] for a in plan["agents"]]
        assert "planner" in roles


class TestDeploymentManifestEndpoint:
    def test_generate_manifest(self, client: TestClient, structured_intake) -> None:
        norm_resp = client.post("/api/process/normalize", json=structured_intake.model_dump())
        normalized = norm_resp.json()

        manifest_resp = client.post(
            "/api/deployment/manifest",
            json={"process": normalized, "environment": "dev"},
        )
        assert manifest_resp.status_code == 200
        manifest = manifest_resp.json()
        assert "resources" in manifest
        assert manifest["environment"] == "dev"

    def test_manifest_has_container_apps(self, client: TestClient, structured_intake) -> None:
        norm_resp = client.post("/api/process/normalize", json=structured_intake.model_dump())
        normalized = norm_resp.json()
        manifest_resp = client.post(
            "/api/deployment/manifest",
            json={"process": normalized},
        )
        manifest = manifest_resp.json()
        assert len(manifest["resources"]["container_apps"]) >= 2


class TestPipelineEndpoint:
    def test_full_pipeline(self, client: TestClient, structured_intake) -> None:
        response = client.post("/api/process/pipeline", json=structured_intake.model_dump())
        assert response.status_code == 200
        data = response.json()
        assert "normalized_process" in data
        assert "process_graph" in data
        assert "agent_plan" in data
        assert "deployment_manifest" in data

    def test_pipeline_process_id_consistent(self, client: TestClient, structured_intake) -> None:
        response = client.post("/api/process/pipeline", json=structured_intake.model_dump())
        data = response.json()
        process_id = data["normalized_process"]["id"]
        assert data["process_graph"]["process_id"] == process_id
        assert data["agent_plan"]["process_id"] == process_id
        assert data["deployment_manifest"]["process_id"] == process_id
