# Shared Schemas

This package contains the JSON schemas and TypeScript type definitions that are shared between the API and web apps.

## JSON Schemas

| Schema | File | Description |
|--------|------|-------------|
| Process Intake | `json/process-intake.schema.json` | Intake payload (freeform or structured BYOP) |
| Normalized Process | `json/normalized-process.schema.json` | Canonical intermediate process model |
| Process Graph | `json/process-graph.schema.json` | Node/edge graph for rendering |
| Agent Plan | `json/agent-plan.schema.json` | Azure AI Foundry agent orchestration design |
| Deployment Manifest | `json/deployment-manifest.schema.json` | Azure resource deployment specification |

## Usage

### In Python (via Pydantic)

The API app uses Pydantic v2 models that correspond 1:1 with these JSON schemas.
See `apps/api/app/models/` for the Pydantic model definitions.

### In TypeScript

Import types from `src/lib/api.ts` in the web app. In a future phase, these will be auto-generated from the JSON schemas using `json-schema-to-typescript`.

## Schema design principles

1. **Schema-first** — schemas are the authoritative contract. Code is derived from schemas, not vice versa.
2. **Process-agnostic** — schemas are domain-independent and support any business process.
3. **Linked by process ID** — all outputs (graph, agent plan, manifest) reference the normalized process via `process_id`.
4. **Versioned** — all schemas include a `schema_version` field for future evolution.
