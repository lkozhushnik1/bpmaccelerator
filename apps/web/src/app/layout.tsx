import type { Metadata } from 'next'
import './globals.css'
import { NavBar } from '@/components/ui/NavBar'

export const metadata: Metadata = {
  title: 'BPM Accelerator',
  description:
    'Transform any business process into a normalized model, visual graph, Azure AI Foundry agent plan, and deployment artifacts.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans bg-gray-50 min-h-screen antialiased">
        <NavBar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
      </body>
    </html>
  )
}
