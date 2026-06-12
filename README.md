# BPM Accelerator

> **A prompt-driven Business Process Mapping Accelerator** that transforms any business process description into a normalized process model, visual graph, Azure AI Foundry agent plan, and Azure deployment artifacts as code.

[![CI – API](https://github.com/lkozhushnik1/bpmaccelerator/actions/workflows/api.yml/badge.svg)](https://github.com/lkozhushnik1/bpmaccelerator/actions/workflows/api.yml)
[![CI – Web](https://github.com/lkozhushnik1/bpmaccelerator/actions/workflows/web.yml/badge.svg)](https://github.com/lkozhushnik1/bpmaccelerator/actions/workflows/web.yml)

---

## What it does

1. **Accept any business process** — via freeform prompt or structured "Bring Your Own Process" intake.
2. **Normalize** it into a canonical, schema-validated process model.
3. **Generate** a visual process graph ready for editing.
4. **Design** an Azure AI Foundry multi-agent orchestration plan.
5. **Produce** Azure deployment artifacts (Bicep IaC) as code.

---

## Repository structure

```text
bpmaccelerator/
├── apps/
│   ├── api/          # Python FastAPI backend
│   └── web/          # Next.js TypeScript frontend
├── packages/
│   └── schemas/      # Shared JSON schemas + TypeScript types
├── infra/
│   └── bicep/        # Azure Bicep infrastructure templates
├── docs/             # Architecture and product documentation
├── examples/         # Sample process payloads and generated outputs
└── .github/
    └── workflows/    # CI pipelines
```

---

## Quick start

### Frontend-only (demo mode) — no backend needed

This is the fastest way to explore the UI:

```bash
cd apps/web
npm install
npm run dev:demo
```

Open `http://localhost:3000` — the app loads pre-built fixture data (the Cloud
Cost Anomaly Detection golden example) without calling the API. A banner at the
top of every page confirms demo mode is active.

To enable demo mode manually (e.g. from a `.env.local` file):

```bash
cp apps/web/.env.local.example apps/web/.env.local
# .env.local already has NEXT_PUBLIC_DEMO_MODE=true
cd apps/web && npm run dev
```

---

### Full stack (frontend + backend)

**Prerequisites:** Node.js 20+, Python 3.11+

#### 1. Backend (FastAPI)

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API is now available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

#### 2. Frontend (Next.js)

```bash
cd apps/web
npm install
npm run dev
```

App is now available at `http://localhost:3000`.

---

## Key API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/process/normalize` | Normalize intake → process model |
| POST | `/api/process/graph` | Process model → graph JSON |
| POST | `/api/agents/plan` | Process model → agent plan |
| POST | `/api/deployment/manifest` | Process model → deployment manifest |
| POST | `/api/process/pipeline` | Full pipeline (normalize → graph → agents → manifest) |

---

## Golden example

The **Cloud Cost Anomaly Detection and Remediation** process (Financial Services / Insurance) is the primary reference example. See [`examples/`](./examples/) for intake and all generated output artefacts.

---

## Documentation

| Document | Description |
|----------|-------------|
| [docs/architecture.md](./docs/architecture.md) | End-to-end architecture overview |
| [docs/product-requirements.md](./docs/product-requirements.md) | Full product requirements |

---

## Roadmap

| Phase | Focus |
|-------|-------|
| **1 – Scaffold** *(current)* | Schema-first model, placeholder transformation, basic UI |
| **2 – Intelligence** | Real Azure AI Foundry agent integration, LLM-backed normalization |
| **3 – Deploy** | One-click Azure deployment, ITSM integrations, BPMN export |
