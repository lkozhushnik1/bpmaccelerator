'use client'

interface GraphNode {
  id: string
  label: string
  node_type: string
  is_automated: boolean
  automation_candidate: boolean
  actor_ids?: string[]
}

interface GraphEdge {
  id: string
  source: string
  target: string
  label?: string
  edge_type: string
}

const NODE_TYPE_STYLES: Record<string, string> = {
  start: 'bg-gray-800 text-white',
  end: 'bg-gray-800 text-white',
  task: 'bg-blue-100 text-blue-900 border-blue-300',
  decision: 'bg-yellow-100 text-yellow-900 border-yellow-300',
  approval: 'bg-orange-100 text-orange-900 border-orange-300',
  integration: 'bg-purple-100 text-purple-900 border-purple-300',
  validation: 'bg-green-100 text-green-900 border-green-300',
  notification: 'bg-cyan-100 text-cyan-900 border-cyan-300',
}

export function GraphPreview({ graph }: { graph: Record<string, unknown> }) {
  const nodes = (graph?.nodes as GraphNode[]) ?? []
  const edges = (graph?.edges as GraphEdge[]) ?? []
  const swimlanes = (graph?.swimlanes as { id: string; label: string; node_ids: string[] }[]) ?? []

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-900">Process Graph</h3>
          <p className="text-sm text-gray-500">
            {nodes.length} nodes · {edges.length} edges · {swimlanes.length} swimlanes
          </p>
        </div>
        <div className="text-xs text-amber-600 bg-amber-50 border border-amber-200 px-3 py-1.5 rounded-lg">
          📌 Interactive graph visualization coming in Phase 2
        </div>
      </div>

      {/* Swimlanes */}
      {swimlanes.length > 0 && (
        <section className="space-y-3">
          <h4 className="text-sm font-medium text-gray-700">Swimlanes</h4>
          <div className="space-y-2">
            {swimlanes.map((lane) => (
              <div key={lane.id} className="rounded-lg border border-gray-200 overflow-hidden">
                <div className="px-4 py-2 bg-gray-50 border-b border-gray-200 text-sm font-medium text-gray-700">
                  {lane.label}
                </div>
                <div className="px-4 py-2 flex flex-wrap gap-2">
                  {lane.node_ids.map((nid) => {
                    const node = nodes.find((n) => n.id === nid)
                    return node ? (
                      <span
                        key={nid}
                        className={`text-xs px-2 py-1 rounded border font-medium ${
                          NODE_TYPE_STYLES[node.node_type] ?? 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        {node.label}
                      </span>
                    ) : null
                  })}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Node list */}
      <section className="space-y-3">
        <h4 className="text-sm font-medium text-gray-700">Nodes</h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
          {nodes.map((node) => (
            <div
              key={node.id}
              className={`rounded-lg border px-3 py-2 text-sm flex items-center gap-2 ${
                NODE_TYPE_STYLES[node.node_type] ?? 'bg-gray-50 text-gray-700 border-gray-200'
              }`}
            >
              <span className="font-medium truncate">{node.label}</span>
              {node.automation_candidate && (
                <span className="text-[10px] shrink-0">🤖</span>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Edge list */}
      <section className="space-y-3">
        <h4 className="text-sm font-medium text-gray-700">Edges ({edges.length})</h4>
        <div className="space-y-1 max-h-48 overflow-y-auto text-xs font-mono text-gray-600">
          {edges.map((edge) => (
            <div key={edge.id} className="flex items-center gap-2">
              <span className="truncate max-w-[120px]">{edge.source}</span>
              <span className="text-gray-400">→</span>
              <span className="truncate max-w-[120px]">{edge.target}</span>
              {edge.label && (
                <span className="text-amber-600 italic">[{edge.label}]</span>
              )}
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
