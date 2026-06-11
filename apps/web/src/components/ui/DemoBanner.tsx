/**
 * DemoBanner — shown at the top of every page when NEXT_PUBLIC_DEMO_MODE=true.
 * This is a server component; the env var is inlined at build time.
 */
export function DemoBanner() {
  if (process.env.NEXT_PUBLIC_DEMO_MODE !== 'true') return null

  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2 text-center text-sm text-amber-800">
      <span className="font-semibold">Demo mode</span> — the app is running with
      pre-built fixture data. No backend required.{' '}
      <a
        href="https://github.com/lkozhushnik1/bpmaccelerator#quick-start"
        target="_blank"
        rel="noopener noreferrer"
        className="underline hover:text-amber-900"
      >
        Start the API
      </a>{' '}
      and remove <code className="font-mono text-xs">NEXT_PUBLIC_DEMO_MODE</code>{' '}
      to use live data.
    </div>
  )
}
