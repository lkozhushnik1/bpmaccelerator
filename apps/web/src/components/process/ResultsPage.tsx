'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { cn } from '@/lib/utils'
import { JsonViewer } from './JsonViewer'
import { ProcessSummary } from './ProcessSummary'
import { GraphPreview } from './GraphPreview'
import { AgentPlanPreview } from './AgentPlanPreview'
import { DeploymentManifestPreview } from './DeploymentManifestPreview'

type Tab = 'process' | 'graph' | 'agents' | 'deployment'

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: 'process', label: 'Normalized Process', icon: '🗂️' },
  { id: 'graph', label: 'Process Graph', icon: '🔀' },
  { id: 'agents', label: 'Agent Plan', icon: '🤖' },
  { id: 'deployment', label: 'Deployment', icon: '☁️' },
]

export function ResultsPage() {
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const [activeTab, setActiveTab] = useState<Tab>('process')
  const [jsonMode, setJsonMode] = useState(false)

  useEffect(() => {
    const stored = sessionStorage.getItem('bpmacc_result')
    if (stored) {
      try {
        setResult(JSON.parse(stored))
      } catch {
        // ignore parse errors
      }
    }
  }, [])

  if (!result) {
    return (
      <div className="max-w-2xl mx-auto text-center py-24 space-y-6">
        <div className="text-5xl">🗂️</div>
        <h1 className="text-2xl font-bold text-gray-900">No results yet</h1>
        <p className="text-gray-600">
          Submit a process from the intake page to see generated artifacts here.
        </p>
        <Link href="/intake" className="btn-primary">
          Go to intake →
        </Link>
      </div>
    )
  }

  const normalized = result.normalized_process as Record<string, unknown>
  const graph = result.process_graph as Record<string, unknown>
  const agentPlan = result.agent_plan as Record<string, unknown>
  const manifest = result.deployment_manifest as Record<string, unknown>

  const processName =
    (normalized?.metadata as Record<string, unknown>)?.name ?? 'Process'

  const activeData: Record<string, unknown> = {
    process: normalized,
    graph,
    agents: agentPlan,
    deployment: manifest,
  }[activeTab] as Record<string, unknown>

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Link href="/intake" className="hover:text-gray-700">
              ← New process
            </Link>
          </div>
          <h1 className="text-2xl font-bold text-gray-900 truncate max-w-xl">
            {processName as string}
          </h1>
        </div>
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => setJsonMode((v) => !v)}
            className="btn-secondary text-xs"
          >
            {jsonMode ? 'Rich view' : 'JSON view'}
          </button>
          <button
            type="button"
            onClick={() => {
              const blob = new Blob(
                [JSON.stringify(result, null, 2)],
                { type: 'application/json' },
              )
              const url = URL.createObjectURL(blob)
              const a = document.createElement('a')
              a.href = url
              a.download = 'bpmacc-output.json'
              a.click()
              URL.revokeObjectURL(url)
            }}
            className="btn-secondary text-xs"
          >
            ↓ Download all
          </button>
          <Link href="/intake" className="btn-primary text-xs">
            New process
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-0 border-b border-gray-200 overflow-x-auto">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            onClick={() => setActiveTab(tab.id)}
            className={cn(
              'px-5 py-3 text-sm font-medium whitespace-nowrap',
              activeTab === tab.id ? 'tab-active' : 'tab-inactive',
            )}
          >
            <span className="mr-1.5">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="card overflow-hidden">
        {jsonMode ? (
          <JsonViewer data={activeData} />
        ) : (
          <>
            {activeTab === 'process' && (
              <ProcessSummary process={normalized} />
            )}
            {activeTab === 'graph' && <GraphPreview graph={graph} />}
            {activeTab === 'agents' && (
              <AgentPlanPreview plan={agentPlan} />
            )}
            {activeTab === 'deployment' && (
              <DeploymentManifestPreview manifest={manifest} />
            )}
          </>
        )}
      </div>
    </div>
  )
}
