'use client'

interface AgentTool {
  name: string
  tool_type: string
  description?: string
}

interface Agent {
  id: string
  name: string
  role: string
  description?: string
  trigger: string
  inputs: string[]
  outputs: string[]
  tools: AgentTool[]
  human_in_loop: boolean
}

interface HumanCheckpoint {
  id: string
  name: string
  description?: string
  after_agent_id: string
}

const ROLE_STYLES: Record<string, string> = {
  planner: 'bg-indigo-100 text-indigo-700 border-indigo-200',
  specialist: 'bg-blue-100 text-blue-700 border-blue-200',
  validator: 'bg-green-100 text-green-700 border-green-200',
  human_proxy: 'bg-orange-100 text-orange-700 border-orange-200',
}

export function AgentPlanPreview({ plan }: { plan: Record<string, unknown> }) {
  const agents = (plan?.agents as Agent[]) ?? []
  const checkpoints = (plan?.human_checkpoints as HumanCheckpoint[]) ?? []
  const pattern = plan?.orchestration_pattern as string

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <div>
          <h3 className="font-semibold text-gray-900">Agent Plan</h3>
          <p className="text-sm text-gray-500">
            {agents.length} agents · {checkpoints.length} human checkpoints
          </p>
        </div>
        {pattern && (
          <span className="text-xs px-3 py-1.5 rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200 font-medium">
            {pattern.replaceAll('_', ' ')}
          </span>
        )}
      </div>

      {/* Agents */}
      <div className="space-y-4">
        {agents.map((agent) => (
          <div key={agent.id} className="rounded-xl border border-gray-200 overflow-hidden">
            <div className="px-4 py-3 flex items-center gap-3 bg-gray-50 border-b border-gray-100">
              <span className="text-lg">{agent.role === 'planner' ? '🧠' : agent.role === 'validator' ? '✅' : agent.human_in_loop ? '👤' : '🤖'}</span>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-medium text-gray-900">{agent.name}</span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded border ${
                      ROLE_STYLES[agent.role] ?? 'bg-gray-100 text-gray-600 border-gray-200'
                    }`}
                  >
                    {agent.role}
                  </span>
                  {agent.human_in_loop && (
                    <span className="text-xs px-2 py-0.5 rounded border bg-amber-50 text-amber-700 border-amber-200">
                      👤 human-in-loop
                    </span>
                  )}
                </div>
                {agent.description && (
                  <p className="text-xs text-gray-500 mt-0.5">{agent.description}</p>
                )}
              </div>
            </div>
            <div className="px-4 py-3 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div>
                <span className="font-medium text-gray-700 block mb-1">Trigger</span>
                <p className="text-gray-600">{agent.trigger}</p>
              </div>
              <div>
                <span className="font-medium text-gray-700 block mb-1">
                  Inputs / Outputs
                </span>
                <p className="text-gray-600">
                  {agent.inputs.join(', ')} → {agent.outputs.join(', ')}
                </p>
              </div>
              <div>
                <span className="font-medium text-gray-700 block mb-1">Tools</span>
                <div className="flex flex-wrap gap-1">
                  {agent.tools.map((t) => (
                    <span
                      key={t.name}
                      title={t.description}
                      className="px-1.5 py-0.5 rounded bg-gray-100 text-gray-700"
                    >
                      {t.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Human checkpoints */}
      {checkpoints.length > 0 && (
        <section className="space-y-2">
          <h4 className="font-medium text-gray-900 text-sm">Human Checkpoints</h4>
          <div className="space-y-2">
            {checkpoints.map((cp) => (
              <div
                key={cp.id}
                className="flex items-start gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3"
              >
                <span className="text-amber-500 text-lg shrink-0">⏸</span>
                <div>
                  <p className="font-medium text-amber-900 text-sm">{cp.name}</p>
                  {cp.description && (
                    <p className="text-amber-700 text-xs mt-0.5">{cp.description}</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
