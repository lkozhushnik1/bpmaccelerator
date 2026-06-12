import { DEMO_PIPELINE_RESULT } from './mock-data'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * When NEXT_PUBLIC_DEMO_MODE=true the app returns pre-built fixture data
 * instead of calling the backend. This lets you explore the full UI without
 * needing a running API server.
 */
const DEMO_MODE = process.env.NEXT_PUBLIC_DEMO_MODE === 'true'

export interface ProcessIntake {
  mode: 'freeform' | 'structured'
  prompt?: string
  industry?: string
  process_name?: string
  departments?: string[]
  overview?: string
  key_steps?: string[]
  pain_points?: string[]
  automation_goals?: string[]
  systems?: string[]
  approvals?: string[]
  risks?: string[]
  constraints?: string[]
  success_metrics?: string[]
}

export interface PipelineResult {
  normalized_process: Record<string, unknown>
  process_graph: Record<string, unknown>
  agent_plan: Record<string, unknown>
  deployment_manifest: Record<string, unknown>
}

export async function runPipeline(intake: ProcessIntake): Promise<PipelineResult> {
  if (DEMO_MODE) {
    // Simulate a short network delay so the loading state is visible
    await new Promise((resolve) => setTimeout(resolve, 800))
    return DEMO_PIPELINE_RESULT as PipelineResult
  }

  const res = await fetch(`${API_URL}/api/process/pipeline`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(intake),
  })
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

export async function normalizeProcess(
  intake: ProcessIntake,
): Promise<Record<string, unknown>> {
  if (DEMO_MODE) {
    await new Promise((resolve) => setTimeout(resolve, 400))
    return DEMO_PIPELINE_RESULT.normalized_process as Record<string, unknown>
  }

  const res = await fetch(`${API_URL}/api/process/normalize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(intake),
  })
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}
