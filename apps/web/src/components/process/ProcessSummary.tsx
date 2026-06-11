'use client'

interface Step {
  id: string
  name: string
  description?: string
  sequence: number
  step_type: string
  is_automated: boolean
  automation_candidate: boolean
  actor_ids?: string[]
  system_refs?: string[]
}

interface Actor {
  id: string
  name: string
  role_type: string
}

interface System {
  id: string
  name: string
  system_type: string
  vendor?: string
}

interface KPI {
  id: string
  name: string
  target?: string
  unit?: string
}

const STEP_TYPE_COLORS: Record<string, string> = {
  task: 'bg-blue-50 text-blue-700 border-blue-200',
  decision: 'bg-yellow-50 text-yellow-700 border-yellow-200',
  approval: 'bg-orange-50 text-orange-700 border-orange-200',
  integration: 'bg-purple-50 text-purple-700 border-purple-200',
  validation: 'bg-green-50 text-green-700 border-green-200',
  notification: 'bg-cyan-50 text-cyan-700 border-cyan-200',
  start: 'bg-gray-50 text-gray-700 border-gray-200',
  end: 'bg-gray-50 text-gray-700 border-gray-200',
}

export function ProcessSummary({
  process,
}: {
  process: Record<string, unknown>
}) {
  const metadata = process.metadata as Record<string, unknown>
  const overview = process.overview as Record<string, unknown>
  const steps = (process.steps as Step[]) ?? []
  const actors = (process.actors as Actor[]) ?? []
  const systems = (process.systems as System[]) ?? []
  const kpis = (process.kpis as KPI[]) ?? []
  const painPoints = (process.pain_points as { id: string; description: string }[]) ?? []
  const automationGoals = (process.automation_goals as string[]) ?? []

  const actorMap: Record<string, string> = {}
  for (const a of actors) actorMap[a.id] = a.name

  return (
    <div className="p-6 space-y-8">
      {/* Overview */}
      <section className="space-y-3">
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{metadata?.name as string}</h2>
            {(metadata?.industry as string | undefined) && (
              <p className="text-sm text-gray-500">{metadata.industry as string}</p>
            )}
          </div>
          <div className="flex flex-wrap gap-2">
            {((metadata?.departments as string[]) ?? []).map((d) => (
              <span
                key={d}
                className="text-xs px-2 py-1 rounded-full bg-brand-100 text-brand-700"
              >
                {d}
              </span>
            ))}
          </div>
        </div>
        <p className="text-gray-700 text-sm leading-relaxed">
          {overview?.description as string}
        </p>
        {(overview?.objectives as string[])?.length > 0 && (
          <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
            {(overview.objectives as string[]).map((o, i) => (
              <li key={i}>{o}</li>
            ))}
          </ul>
        )}
      </section>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Steps', value: steps.length },
          { label: 'Actors', value: actors.length },
          { label: 'Systems', value: systems.length },
          {
            label: 'Auto candidates',
            value: steps.filter((s) => s.automation_candidate).length,
          },
        ].map((s) => (
          <div key={s.label} className="rounded-lg bg-gray-50 border border-gray-100 p-4 text-center">
            <div className="text-2xl font-bold text-gray-900">{s.value}</div>
            <div className="text-xs text-gray-500 mt-1">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Steps */}
      <section className="space-y-3">
        <h3 className="font-semibold text-gray-900">Process Steps</h3>
        <div className="space-y-2">
          {steps.map((step) => (
            <div
              key={step.id}
              className="flex items-start gap-4 p-3 rounded-lg border border-gray-100 hover:border-gray-200 transition-colors"
            >
              <span className="shrink-0 w-7 h-7 rounded-full bg-gray-100 text-gray-600 text-xs font-bold flex items-center justify-center">
                {step.sequence}
              </span>
              <div className="flex-1 min-w-0 space-y-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-medium text-sm text-gray-900">{step.name}</span>
                  <span
                    className={`text-xs px-1.5 py-0.5 rounded border font-medium ${
                      STEP_TYPE_COLORS[step.step_type] ?? 'bg-gray-50 text-gray-600 border-gray-200'
                    }`}
                  >
                    {step.step_type}
                  </span>
                  {step.automation_candidate && (
                    <span className="text-xs px-1.5 py-0.5 rounded border bg-emerald-50 text-emerald-700 border-emerald-200">
                      🤖 auto candidate
                    </span>
                  )}
                </div>
                <div className="flex flex-wrap gap-2 text-xs text-gray-500">
                  {step.actor_ids?.map((id) => (
                    <span key={id} className="flex items-center gap-1">
                      👤 {actorMap[id] ?? id}
                    </span>
                  ))}
                  {step.system_refs?.map((s) => (
                    <span key={s} className="flex items-center gap-1">
                      🔧 {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Pain Points & Goals */}
      {painPoints.length > 0 && (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <h3 className="font-semibold text-gray-900">Pain Points</h3>
            <ul className="space-y-1">
              {painPoints.map((pp) => (
                <li key={pp.id} className="text-sm text-gray-600 flex gap-2">
                  <span className="text-red-400 shrink-0">⚠</span>
                  {pp.description}
                </li>
              ))}
            </ul>
          </div>
          {automationGoals.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-semibold text-gray-900">Automation Goals</h3>
              <ul className="space-y-1">
                {automationGoals.map((g, i) => (
                  <li key={i} className="text-sm text-gray-600 flex gap-2">
                    <span className="text-green-500 shrink-0">✓</span>
                    {g}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      )}

      {/* Systems & KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {systems.length > 0 && (
          <div className="space-y-2">
            <h3 className="font-semibold text-gray-900">Systems</h3>
            <div className="flex flex-wrap gap-2">
              {systems.map((s) => (
                <span
                  key={s.id}
                  title={s.vendor ?? s.system_type}
                  className="text-xs px-2 py-1 rounded bg-gray-100 text-gray-700"
                >
                  {s.name}
                </span>
              ))}
            </div>
          </div>
        )}
        {kpis.length > 0 && (
          <div className="space-y-2">
            <h3 className="font-semibold text-gray-900">KPIs</h3>
            <ul className="space-y-1">
              {kpis.map((k) => (
                <li key={k.id} className="text-sm text-gray-700 flex justify-between gap-2">
                  <span>{k.name}</span>
                  {k.target && (
                    <span className="text-gray-500 text-xs">
                      {k.target} {k.unit}
                    </span>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
