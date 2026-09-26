import { useEffect, useState } from 'react'
import { fetchHealth } from '../lib/api'

function HealthChip() {
  const [engine, setEngine] = useState<string | null>(null)
  const [offline, setOffline] = useState(false)

  useEffect(() => {
    fetchHealth()
      .then((h) => setEngine(h.engine))
      .catch(() => setOffline(true))
  }, [])

  if (offline) {
    return (
      <span className="flex items-center gap-1.5 rounded-full border border-bad/40 bg-bad/10 px-2.5 py-1 font-mono text-[10px] text-bad">
        <span className="h-1.5 w-1.5 rounded-full bg-bad" />
        ENGINE OFFLINE
      </span>
    )
  }
  return (
    <span className="flex items-center gap-1.5 rounded-full border border-ok/40 bg-ok/10 px-2.5 py-1 font-mono text-[10px] text-ok">
      <span className="h-1.5 w-1.5 rounded-full bg-ok" />
      ENGINE {engine ? `v${engine}` : '…'}
    </span>
  )
}

export default function Topbar() {
  return (
    <header className="flex h-12 shrink-0 items-center gap-3 border-b border-border bg-panel px-4">
      <div className="flex items-center gap-2 text-[13px]">
        <span className="font-medium">Atlas Rover</span>
        <span className="rounded-full border border-border px-2 py-0.5 font-mono text-[10px] text-text-2">
          v2.3.1
        </span>
        <span className="font-mono text-[11px] text-text-3">main @ a83fd21</span>
      </div>
      <div className="ml-auto flex items-center gap-3">
        <div className="flex w-64 items-center gap-2 rounded-md border border-border bg-bg px-3 py-1.5 text-[12px] text-text-3">
          <span className="material-symbols-outlined !text-[16px]">search</span>
          <span className="truncate">Search modules, files, robots…</span>
          <kbd className="ml-auto rounded border border-border px-1 font-mono text-[10px]">⌘K</kbd>
        </div>
        <HealthChip />
      </div>
    </header>
  )
}
