"""BPM Accelerator — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import health, process, agents, deployment

app = FastAPI(
    title="BPM Accelerator API",
    description=(
        "Transforms any business process description into a normalized process model, "
        "visual graph, Azure AI Foundry agent plan, and Azure deployment artifacts."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(process.router, prefix="/api/process", tags=["process"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(deployment.router, prefix="/api/deployment", tags=["deployment"])
