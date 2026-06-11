'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { type ProcessIntake, runPipeline } from '@/lib/api'
import { cn } from '@/lib/utils'

type Mode = 'freeform' | 'structured'

export function IntakePage() {
  const router = useRouter()
  const [mode, setMode] = useState<Mode>('structured')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // Freeform
  const [prompt, setPrompt] = useState('')

  // Structured fields
  const [industry, setIndustry] = useState('')
  const [processName, setProcessName] = useState('')
  const [departments, setDepartments] = useState('')
  const [overview, setOverview] = useState('')
  const [keySteps, setKeySteps] = useState('')
  const [painPoints, setPainPoints] = useState('')
  const [automationGoals, setAutomationGoals] = useState('')
  const [systems, setSystems] = useState('')
  const [approvals, setApprovals] = useState('')
  const [successMetrics, setSuccessMetrics] = useState('')

  const splitLines = (v: string) =>
    v
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      const intake: ProcessIntake =
        mode === 'freeform'
          ? { mode: 'freeform', prompt }
          : {
              mode: 'structured',
              industry: industry || undefined,
              process_name: processName,
              departments: splitLines(departments),
              overview,
              key_steps: splitLines(keySteps),
              pain_points: splitLines(painPoints),
              automation_goals: splitLines(automationGoals),
              systems: splitLines(systems),
              approvals: splitLines(approvals),
              success_metrics: splitLines(successMetrics),
            }

      const result = await runPipeline(intake)
      sessionStorage.setItem('bpmacc_result', JSON.stringify(result))
      router.push('/results')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.')
    } finally {
      setLoading(false)
    }
  }

  const loadExample = () => {
    setMode('structured')
    setIndustry('Financial Services (Insurance)')
    setProcessName('Cloud Cost Anomaly Detection and Remediation')
    setDepartments(
      'FinOps\nCloud Platform Engineering\nApplication Teams\nObservability (Splunk/New Relic)\nIT Service Management (ServiceNow)',
    )
    setOverview(
      'Identifies and resolves unexpected increases in cloud spend across hybrid environments by correlating cost signals with infrastructure changes, utilisation metrics, and observability data to determine root cause.',
    )
    setKeySteps(
      'Detect cost anomaly\nCorrelate infrastructure changes\nCorrelate observability data\nIdentify top cost drivers\nRoot cause analysis\nClassify issue type\nGenerate remediation actions\nRank actions by impact and risk\nRoute to team owners\nCreate ServiceNow tickets\nRequest approvals\nExecute approved actions\nValidate outcomes\nClose tickets and update baseline',
    )
    setPainPoints(
      'Fragmented tooling across AWS, Splunk, New Relic, and ServiceNow\nSlow manual analysis taking hours to days\nApproval bottlenecks slowing execution\nNo closed-loop validation',
    )
    setAutomationGoals(
      'Automated closed-loop detect → analyse → act → validate cycle\nAI-driven root cause analysis correlating multiple data sources\nAutomated ticket creation and routing in ServiceNow',
    )
    setSystems('AWS Cost Explorer\nDatabricks\nSplunk\nNew Relic\nServiceNow\nAzure AI Foundry')
    setApprovals('FinOps approval required for any action with cost impact > $1,000/month\nApplication Team owner approval required before changes in their environment')
    setSuccessMetrics(
      'Mean time to detect anomaly < 15 minutes\nMean time to remediate < 4 hours\nFalse positive rate < 5%\nMonthly savings > $50,000',
    )
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold text-gray-900">New Process</h1>
        <p className="text-gray-600">
          Describe any business process and generate a normalized model, graph,
          agent plan, and Azure deployment artifacts.
        </p>
      </div>

      {/* Mode tabs */}
      <div className="flex gap-6 border-b border-gray-200">
        {(['structured', 'freeform'] as const).map((m) => (
          <button
            key={m}
            type="button"
            onClick={() => setMode(m)}
            className={cn(
              'pb-3 text-sm font-medium capitalize',
              mode === m ? 'tab-active' : 'tab-inactive',
            )}
          >
            {m === 'structured' ? '📋 Structured (BYOP)' : '💬 Freeform Prompt'}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {mode === 'freeform' ? (
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700">
              Process description
            </label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={8}
              required
              minLength={10}
              placeholder="Describe your business process in plain language…&#10;&#10;Example: Map out our employee onboarding process — identify approvals, systems touched, and propose AI agents for document collection, access provisioning, and compliance checks."
              className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 resize-y"
            />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex justify-end">
              <button
                type="button"
                onClick={loadExample}
                className="text-sm text-brand-600 hover:text-brand-700 font-medium"
              >
                Load golden example ✨
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Field label="Industry" optional>
                <input
                  value={industry}
                  onChange={(e) => setIndustry(e.target.value)}
                  placeholder="e.g. Financial Services"
                  className="input"
                />
              </Field>
              <Field label="Process Name" required>
                <input
                  value={processName}
                  onChange={(e) => setProcessName(e.target.value)}
                  required
                  placeholder="e.g. Cloud Cost Anomaly Detection"
                  className="input"
                />
              </Field>
            </div>

            <Field label="Departments / Functions involved" optional hint="One per line">
              <textarea
                value={departments}
                onChange={(e) => setDepartments(e.target.value)}
                rows={3}
                placeholder="FinOps&#10;Cloud Platform Engineering&#10;Application Teams"
                className="input resize-y"
              />
            </Field>

            <Field label="Process Overview" required>
              <textarea
                value={overview}
                onChange={(e) => setOverview(e.target.value)}
                required
                rows={4}
                placeholder="2–5 sentence description of the process…"
                className="input resize-y"
              />
            </Field>

            <Field label="Key Steps" optional hint="One per line, in order">
              <textarea
                value={keySteps}
                onChange={(e) => setKeySteps(e.target.value)}
                rows={6}
                placeholder="Detect anomaly&#10;Correlate signals&#10;Root cause analysis&#10;…"
                className="input resize-y"
              />
            </Field>

            <Field label="Pain Points" optional hint="One per line">
              <textarea
                value={painPoints}
                onChange={(e) => setPainPoints(e.target.value)}
                rows={3}
                placeholder="Fragmented tooling&#10;Slow manual analysis&#10;…"
                className="input resize-y"
              />
            </Field>

            <Field label="Automation Goals" optional hint="One per line">
              <textarea
                value={automationGoals}
                onChange={(e) => setAutomationGoals(e.target.value)}
                rows={3}
                placeholder="Automated closed-loop cycle&#10;AI-driven root cause analysis&#10;…"
                className="input resize-y"
              />
            </Field>

            <Field label="Systems / Tools" optional hint="One per line">
              <textarea
                value={systems}
                onChange={(e) => setSystems(e.target.value)}
                rows={3}
                placeholder="ServiceNow&#10;Splunk&#10;AWS Cost Explorer&#10;…"
                className="input resize-y"
              />
            </Field>

            <Field label="Approvals" optional hint="One per line">
              <textarea
                value={approvals}
                onChange={(e) => setApprovals(e.target.value)}
                rows={2}
                placeholder="FinOps approval for actions > $1,000/month&#10;…"
                className="input resize-y"
              />
            </Field>

            <Field label="Success Metrics / KPIs" optional hint="One per line">
              <textarea
                value={successMetrics}
                onChange={(e) => setSuccessMetrics(e.target.value)}
                rows={3}
                placeholder="MTTD < 15 minutes&#10;Monthly savings > $50,000&#10;…"
                className="input resize-y"
              />
            </Field>
          </div>
        )}

        {error && (
          <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <div className="flex items-center gap-4">
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Processing…' : 'Generate artifacts →'}
          </button>
          {loading && (
            <span className="text-sm text-gray-500">
              Running pipeline — normalize → graph → agents → deployment…
            </span>
          )}
        </div>
      </form>
    </div>
  )
}

function Field({
  label,
  required,
  optional,
  hint,
  children,
}: {
  label: string
  required?: boolean
  optional?: boolean
  hint?: string
  children: React.ReactNode
}) {
  return (
    <div className="space-y-1.5">
      <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500">*</span>}
        {optional && (
          <span className="text-xs text-gray-400 font-normal">optional</span>
        )}
        {hint && (
          <span className="text-xs text-gray-400 font-normal">— {hint}</span>
        )}
      </label>
      {children}
    </div>
  )
}
