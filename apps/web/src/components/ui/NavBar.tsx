import Link from 'next/link'

export function NavBar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-xl font-bold text-gray-900">BPM Accelerator</span>
            <span className="hidden sm:inline text-xs px-2 py-0.5 rounded-full bg-brand-100 text-brand-700 font-medium">
              v0.1
            </span>
          </Link>
          <div className="flex items-center gap-6">
            <Link
              href="/intake"
              className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              New Process
            </Link>
            <a
              href="https://github.com/lkozhushnik1/bpmaccelerator"
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
            >
              GitHub
            </a>
            <Link href="/intake" className="btn-primary text-sm">
              Get started
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
