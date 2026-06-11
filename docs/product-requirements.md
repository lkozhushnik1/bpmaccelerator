# Product Requirements — BPM Accelerator

## Vision

A **universal prompt-to-process platform** that transforms any business workflow into a structured operating model, multi-agent solution design in Azure AI Foundry, and deployable Azure infrastructure as code.

---

## Intake modes

### Mode 1: Freeform prompt
The user enters an arbitrary natural-language description of a business process.

Example:
> "Map out our employee onboarding process, identify approvals, systems touched, and propose AI agents for document collection, access provisioning, and compliance checks."

### Mode 2: Structured BYOP ("Bring Your Own Process")
The user fills in structured fields:

| Field | Description |
|-------|-------------|
| Industry | e.g. Financial Services, Healthcare, Retail |
| Process Name | Short descriptive name |
| Departments / Functions | Teams involved |
| Process Overview | 2–5 sentence description |
| Key Steps | Ordered list of major process steps |
| Pain Points | Current problems and inefficiencies |
| Automation Goals | Desired automation outcomes |
| Systems | Tools and platforms involved |
| Approvals | Who approves what, and under which conditions |
| Risks | Known risks and exceptions |
| Constraints | Regulatory, technical, or organizational constraints |
| Success Metrics / KPIs | How success is measured |

Both modes normalize to the same canonical `NormalizedProcess` model.

---

## Required outputs

| Output | Format | Description |
|--------|--------|-------------|
| Normalized process | JSON | Canonical intermediate model |
| Process graph | JSON | Node/edge graph for rendering and editing |
| Agent plan | JSON | Azure AI Foundry agent orchestration design |
| Deployment manifest | JSON | Azure resource deployment specification |

---

## System requirements

### Process-agnostic by default
The system must support any business process without domain-specific hardcoding. Domain templates may be added as optional accelerators in future phases.

### Schema-first design
All data contracts are defined as JSON schemas. API inputs and outputs are validated against these schemas. Agent inputs/outputs are also schema-validated.

### Human-in-the-loop as a first-class concept
Users can review and edit each intermediate artifact before proceeding to the next pipeline stage. No stage is fully automated without a review checkpoint.

### Separation of concerns
Three distinct concerns must remain separated:
1. **Process understanding** — what the process is
2. **Agent design** — how it should be automated
3. **Deployment generation** — what infrastructure to deploy

### Iterative refinement
Users can return to any stage and regenerate downstream artifacts after editing.

---

## Frontend requirements

- Landing page explaining the product
- Intake page with toggle between freeform and structured modes
- Results workspace showing:
  - Normalized process (tabular / JSON view)
  - Process graph (JSON preview with placeholder visualization)
  - Agent plan preview
  - Deployment manifest preview
- Ability to copy or download each artifact
- Clear empty states and loading states
- Responsive layout

---

## Backend requirements

- FastAPI service
- Pydantic v2 models for all inputs and outputs
- Deterministic placeholder transformation logic (Phase 1)
- Input validation with clear error messages
- CORS configured for local development
- OpenAPI docs at `/docs`
- Health endpoint at `/health`

---

## Infrastructure requirements

- Bicep templates for Azure deployment
- Resources: Container Apps or App Service, Storage, Key Vault, Application Insights, Managed Identity
- Environment parameter files (dev, prod)
- No production secrets in templates

---

## Non-functional requirements

- All API responses under 2s for placeholder logic
- Code coverage ≥ 80% for backend transformation logic
- TypeScript strict mode in frontend
- No hardcoded credentials anywhere in the codebase

---

## Golden example

**Industry:** Financial Services (Insurance)  
**Process:** Cloud Cost Anomaly Detection and Remediation  
**Departments:** FinOps, Cloud Platform Engineering, Application Teams, Observability (Splunk/New Relic), ITSM (ServiceNow)

This is the primary example used in documentation, tests, and sample data files. See [`examples/`](../examples/) for the full intake and generated output payloads.

---

## Out of scope (Phase 1)

- Real LLM / AI Foundry integration
- Authentication / authorization
- Persistent storage / database
- BPMN 2.0 export
- Multi-tenant support
- Production deployment pipeline
