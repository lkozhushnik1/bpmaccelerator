import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="space-y-16">
      {/* Hero */}
      <section className="text-center py-16 space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-100 text-brand-700 text-sm font-medium">
          <span className="w-2 h-2 rounded-full bg-brand-600 animate-pulse" />
          Phase 1 — Scaffold
        </div>
        <h1 className="text-5xl font-bold text-gray-900 tracking-tight">
          BPM Accelerator
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Transform <strong>any business process</strong> into a normalized model,
          visual graph, Azure AI&nbsp;Foundry agent plan, and Azure deployment
          artifacts — in seconds.
        </p>
        <div className="flex justify-center gap-4 flex-wrap">
          <Link href="/intake" className="btn-primary text-base px-8 py-3">
            Get started →
          </Link>
          <a
            href="https://github.com/lkozhushnik1/bpmaccelerator"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary text-base px-8 py-3"
          >
            View on GitHub
          </a>
        </div>
      </section>

      {/* How it works */}
      <section className="space-y-8">
        <h2 className="text-2xl font-bold text-gray-900 text-center">How it works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {PIPELINE_STEPS.map((step, i) => (
            <div key={step.title} className="card p-6 space-y-3">
              <div className="w-10 h-10 rounded-lg bg-brand-100 text-brand-700 font-bold text-lg flex items-center justify-center">
                {i + 1}
              </div>
              <h3 className="font-semibold text-gray-900">{step.title}</h3>
              <p className="text-sm text-gray-600">{step.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Intake modes */}
      <section className="space-y-8">
        <h2 className="text-2xl font-bold text-gray-900 text-center">Two intake modes</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card p-6 space-y-3">
            <div className="text-2xl">💬</div>
            <h3 className="font-semibold text-gray-900 text-lg">Freeform prompt</h3>
            <p className="text-gray-600 text-sm">
              Describe any business process in plain language. The accelerator
              extracts structure, steps, actors, and systems automatically.
            </p>
            <p className="text-xs text-gray-400 italic">
              "Map out our cloud cost anomaly detection process and route
              remediations through ServiceNow…"
            </p>
          </div>
          <div className="card p-6 space-y-3">
            <div className="text-2xl">📋</div>
            <h3 className="font-semibold text-gray-900 text-lg">Structured BYOP</h3>
            <p className="text-gray-600 text-sm">
              Fill in structured fields — Industry, Process Name, Departments,
              Key Steps, Pain Points, Systems, and more — for the most accurate
              output.
            </p>
            <p className="text-xs text-gray-400 italic">
              Bring Your Own Process — any domain, any industry.
            </p>
          </div>
        </div>
      </section>

      {/* Outputs */}
      <section className="space-y-8">
        <h2 className="text-2xl font-bold text-gray-900 text-center">Generated outputs</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {OUTPUTS.map((o) => (
            <div key={o.title} className="card p-5 space-y-2">
              <div className="text-2xl">{o.icon}</div>
              <h3 className="font-semibold text-gray-900">{o.title}</h3>
              <p className="text-sm text-gray-600">{o.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="text-center py-8">
        <Link href="/intake" className="btn-primary text-base px-10 py-3">
          Start mapping a process →
        </Link>
      </section>
    </div>
  )
}

const PIPELINE_STEPS = [
  {
    title: 'Describe your process',
    description: 'Use freeform text or fill in structured BYOP fields for any business process.',
  },
  {
    title: 'Normalize',
    description: 'Your input transforms into a canonical process model with steps, actors, and systems.',
  },
  {
    title: 'Design agents',
    description: 'An Azure AI Foundry agent plan is derived with specialist agents and human checkpoints.',
  },
  {
    title: 'Deploy as code',
    description: 'A deployment manifest and Bicep templates are generated for one-click Azure deployment.',
  },
]

const OUTPUTS = [
  {
    icon: '🗂️',
    title: 'Normalized Process',
    description: 'Structured JSON with steps, actors, systems, controls, and KPIs.',
  },
  {
    icon: '🔀',
    title: 'Process Graph',
    description: 'Node/edge graph with swimlanes, ready for editing and visualization.',
  },
  {
    icon: '🤖',
    title: 'Agent Plan',
    description: 'Azure AI Foundry multi-agent orchestration design with tools and checkpoints.',
  },
  {
    icon: '☁️',
    title: 'Deployment Manifest',
    description: 'Azure resource specification for Container Apps, Key Vault, AI Foundry, and more.',
  },
]
