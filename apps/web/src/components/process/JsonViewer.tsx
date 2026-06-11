'use client'

export function JsonViewer({ data }: { data: unknown }) {
  return (
    <pre className="overflow-auto text-xs font-mono bg-gray-900 text-green-300 p-6 rounded-xl max-h-[70vh]">
      {JSON.stringify(data, null, 2)}
    </pre>
  )
}
