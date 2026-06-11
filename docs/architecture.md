# Architecture — BPM Accelerator

## Overview

The BPM Accelerator is a **schema-first, process-agnostic platform** that transforms any business process description into a normalized model, visual graph, Azure AI Foundry agent plan, and deployable Azure infrastructure.

```
┌─────────────────────────────────────────────────────────────────────┐
│                          User Interface (Next.js)                   │
│  ┌──────────────┐  ┌─────────────────────┐  ┌────────────────────┐ │
│  │  Intake Form  │  │   Process Workspace  │  │  Deployment Panel  │ │
│  │ (prompt/BYOP) │  │  (graph, agents)     │  │  (manifest, IaC)   │ │
│  └──────┬───────┘  └──────────┬──────────┘  └────────────────────┘ │
└─────────┼────────────────────┼─────────────────────────────────────┘
          │  REST / JSON        │
┌─────────▼────────────────────▼─────────────────────────────────────┐
│                       API Layer (FastAPI)                           │
│  POST /api/process/normalize   → NormalizedProcess                 │
│  POST /api/process/graph       → ProcessGraph                      │
│  POST /api/agents/plan         → AgentPlan                         │
│  POST /api/deployment/manifest → DeploymentManifest                │
│  POST /api/process/pipeline    → PipelineResult (all four)         │
└─────────────────────────────────────────────────────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────────────────┐
│               Transformation Engine (Python)                       │
│  ┌─────────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Normalizer      │  │ GraphBuilder  │  │ AgentPlanner         │  │
│  │  (intake → model)│  │ (model→graph) │  │ (model → agent plan) │  │
│  └─────────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  DeploymentComposer  (model + agent plan → Bicep manifest)   │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
          │  (Phase 2+)
┌─────────▼─────────────────────────────────────────────────────────┐
│                  Azure AI Foundry                                   │
│  Process Intake Agent  →  Process Mapper Agent                     │
│  Control/Risk Agent    →  Automation Opportunity Agent             │
│  Solution Designer Agent → Deployment Composer Agent               │
└────────────────────────────────────────────────────────────────────┘
```

---

## Canonical process model

All intake formats — freeform prompt or structured BYOP — normalize to the same **NormalizedProcess** schema. This is the single source of truth for all downstream generators.

```
NormalizedProcess
├── metadata        (id, name, version, industry, departments, created_at)
├── overview        (description, objectives[], triggers[], outcomes[])
├── actors[]        (id, name, role_type, systems[])
├── steps[]         (id, name, description, sequence, actor_ids[], system_refs[],
│                    inputs[], outputs[], step_type, is_automated, duration_minutes)
├── decisions[]     (id, name, condition, branches{})
├── artifacts[]     (id, name, artifact_type, format, owner_step_id)
├── controls[]      (id, name, control_type, related_step_ids[], description)
├── pain_points[]   (id, description, affected_steps[])
├── automation_goals[]
├── systems[]       (id, name, system_type, vendor)
├── kpis[]          (id, name, target, unit)
└── metadata_tags   {key: value}
```

---

## Pipeline stages

### Stage 1 – Intake & Normalize
Accepts two input modes:
- **Freeform prompt**: free-text description of any business process.
- **Structured BYOP**: fields including Industry, Process Name, Departments, Overview, Key Steps, Pain Points, Automation Goals, Systems, Approvals, Risks, Constraints, Success Metrics.

Both modes produce a validated `NormalizedProcess` object.

### Stage 2 – Graph Generation
Converts the normalized model into a directed graph:
- nodes represent steps and decisions
- edges represent sequence flow and decision branches
- metadata enables swimlane rendering by actor

### Stage 3 – Agent Plan Generation
Maps automation candidates to Azure AI Foundry agent designs:
- identifies agent roles from step types and automation goals
- assigns tools (API connectors, document processors, search)
- defines human-in-the-loop checkpoints
- specifies orchestration topology (planner + specialists + validator)

### Stage 4 – Deployment Manifest Generation
Produces a structured deployment manifest that can be rendered to Bicep:
- web app (Container App or App Service)
- API app
- AI Foundry workspace reference
- storage account
- Key Vault
- Application Insights / Log Analytics
- managed identity

---

## Human-in-the-loop design

Human review is a first-class concept at each pipeline stage:

1. **After normalization** — review and edit the process model before graph generation.
2. **After graph generation** — edit nodes, edges, and swimlanes before agent planning.
3. **After agent planning** — review and approve agent roles before deployment manifest generation.
4. **After manifest generation** — review and approve IaC before deployment.

The UI workspace provides editing affordances at each stage. The API accepts modified models at each pipeline boundary.

---

## Phase 2: Azure AI Foundry integration

In Phase 2, each transformation stage is backed by a Foundry agent:

| Agent | Responsibility |
|-------|---------------|
| **Process Intake Agent** | Interprets freeform prompt, asks clarifying questions |
| **Process Mapper Agent** | Converts structured entities to ordered workflow |
| **Control/Risk Agent** | Identifies approvals, exceptions, compliance controls |
| **Automation Opportunity Agent** | Identifies steps suitable for AI/automation |
| **Solution Designer Agent** | Maps steps to agent/tool responsibilities |
| **Deployment Composer Agent** | Produces Azure IaC from agent design |

Foundry agents are orchestrated via a Planner → Specialists → Validator pattern with optional human approval gates.

All agent inputs and outputs are schema-validated JSON. Freeform text is never the system's primary contract.

---

## Phase 3: Deployment as code

The deployment manifest JSON drives Bicep template generation:
- `infra/main.bicep` — main entry point
- `infra/modules/` — modular resource definitions
- `infra/parameters/` — environment-specific parameter files
- Generated GitHub Actions workflow for CI/CD

---

## Technology choices

| Concern | Choice | Rationale |
|---------|--------|-----------|
| Frontend | Next.js 14 + TypeScript | Server components, strong ecosystem |
| Styling | Tailwind CSS | Utility-first, fast iteration |
| Backend | Python FastAPI | Async, strong Pydantic integration, Azure SDK ecosystem |
| Validation | Pydantic v2 + JSON Schema | Schema-first contracts |
| IaC | Azure Bicep | Azure-native, readable, strong tooling |
| CI | GitHub Actions | Native to repo |
| Agent orchestration (Ph 2) | Azure AI Foundry | Azure-native multi-agent |
