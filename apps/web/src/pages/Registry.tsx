import { useEffect, useState } from 'react'
import { fetchManifest, fetchModules } from '../lib/api'
import type { ModuleSummary } from '../lib/api'

function LicensePill({ label, id }: { label: string; id: string }) {
  return (
    <span className="rounded-full border border-border px-2 py-0.5 font-mono text-[10px] text-text-2">
      <span className="text-text-3">{label}</span> {id}
    </span>
  )
}

export default function Registry() {
  const [modules, setModules] = useState<ModuleSummary[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState<ModuleSummary | null>(null)
  const [manifest, setManifest] = useState<string | null>(null)

  useEffect(() => {
    fetchModules()
      .then(setModules)
      .catch((e) => setError(String(e)))
  }, [])

  useEffect(() => {
    setManifest(null)
    if (!selected) return
    fetchManifest(selected.id, selected.version)
      .then((doc) => setManifest(JSON.stringify(doc, null, 2)))
      .catch(() => setManifest('// failed to load manifest'))
  }, [selected])

  if (error) {
    return (
      <div className="flex h-full items-center justify-center p-6">
        <div className="max-w-md rounded-[10px] border border-bad/40 bg-bad/5 p-6 text-center">
          <div className="font-mono text-[11px] text-bad">ENGINE OFFLINE</div>
          <p className="mt-2 text-[13px] text-text-2">
            The registry is served by the MERLIN API. Start it and reload:
          </p>
          <pre className="mt-3 rounded-md border border-border bg-bg p-3 text-left font-mono text-[11px] text-text-2">
            cd apps/api{'\n'}uvicorn app.main:app --port 8000
          </pre>
        </div>
      </div>
    )
  }

  const filtered = (modules ?? []).filter((m) => {
    const q = query.toLowerCase()
    return (
      !q ||
      m.id.includes(q) ||
      m.name.toLowerCase().includes(q) ||
      (m.category ?? '').includes(q) ||
      m.tags.some((t) => t.includes(q))
    )
  })

  return (
    <div className="flex h-full">
      <div className="min-w-0 flex-1 space-y-4 overflow-y-auto p-6">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-semibold">Module Registry</h1>
          <span className="flex items-center gap-1.5 rounded-full border border-ok/40 bg-ok/10 px-2.5 py-0.5 font-mono text-[10px] text-ok">
            <span className="h-1.5 w-1.5 rounded-full bg-ok" />
            {modules ? `${modules.length} MODULES · LIVE` : 'LOADING…'}
          </span>
          <div className="ml-auto flex w-56 items-center gap-2 rounded-md border border-border bg-bg px-3 py-1.5">
            <span className="material-symbols-outlined !text-[16px] text-text-3">search</span>
            <input
              id="registry-filter"
              name="registry-filter"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Filter modules…"
              className="w-full bg-transparent text-[12px] text-text outline-none placeholder:text-text-3"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
          {filtered.map((m) => (
            <button
              key={`${m.id}@${m.version}`}
              onClick={() => setSelected(m)}
              className={`rounded-[10px] border bg-panel p-4 text-left transition-colors hover:border-accent/60 ${
                selected?.id === m.id ? 'border-accent' : 'border-border'
              }`}
            >
              <div className="flex items-center gap-2">
                <span className="text-[13px] font-medium">{m.name}</span>
                {m.category && (
                  <span className="rounded-full border border-info/40 bg-info/10 px-2 py-0.5 font-mono text-[10px] text-info">
                    {m.category}
                  </span>
                )}
              </div>
              <div className="mt-0.5 font-mono text-[10px] text-text-3">
                {m.id}@{m.version}
              </div>
              <p className="mt-2 line-clamp-2 min-h-8 text-[12px] text-text-2">{m.description}</p>
              <div className="mt-2 flex gap-3 font-mono text-[11px] text-text-2">
                {m.mass_kg != null && <span>{m.mass_kg} kg</span>}
                {m.power_budget != null && m.power_budget.consumes_w > 0 && (
                  <span>{m.power_budget.consumes_w} W</span>
                )}
                {m.power_budget != null && m.power_budget.provides_w > 0 && (
                  <span className="text-ok">+{m.power_budget.provides_w} W</span>
                )}
              </div>
              <div className="mt-2 flex flex-wrap gap-1">
                {m.compat.slice(0, 2).map((c) => (
                  <span
                    key={c}
                    className="rounded border border-info/30 bg-info/5 px-1.5 py-0.5 font-mono text-[9px] text-info"
                  >
                    {c}
                  </span>
                ))}
                {m.compat.length > 2 && (
                  <span className="font-mono text-[9px] text-text-3">+{m.compat.length - 2}</span>
                )}
              </div>
              <div className="mt-3 flex flex-wrap gap-1 border-t border-border pt-2">
                {m.licenses.hardware && <LicensePill label="HW" id={m.licenses.hardware} />}
                {m.licenses.software && <LicensePill label="SW" id={m.licenses.software} />}
                {m.licenses.docs && <LicensePill label="DOC" id={m.licenses.docs} />}
              </div>
            </button>
          ))}
        </div>
      </div>

      {selected && (
        <aside className="flex w-[380px] shrink-0 flex-col border-l border-border bg-panel">
          <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <div>
              <div className="text-[13px] font-medium">{selected.name}</div>
              <div className="font-mono text-[10px] text-text-3">
                {selected.id}@{selected.version}
              </div>
            </div>
            <button
              onClick={() => setSelected(null)}
              className="rounded-md p-1 text-text-3 hover:bg-panel-2 hover:text-text"
              aria-label="Close"
            >
              <span className="material-symbols-outlined !text-[18px]">close</span>
            </button>
          </div>
          <div className="min-h-0 flex-1 overflow-y-auto p-4">
            <div className="mb-2 font-mono text-[10px] tracking-wider text-text-3 uppercase">
              Manifest
            </div>
            <pre className="rounded-md border border-border bg-bg p-3 font-mono text-[10px] leading-relaxed whitespace-pre-wrap text-text-2">
              {manifest ?? 'loading…'}
            </pre>
          </div>
        </aside>
      )}
    </div>
  )
}
