const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

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
