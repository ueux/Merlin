export interface ModuleSummary {
  id: string
  version: string
  name: string
  category: string | null
  vendor: string | null
  description: string
  tags: string[]
  licenses: Record<string, string>
  mass_kg: number | null
  power_budget: { consumes_w: number; provides_w: number } | null
  interfaces: string[]
  compat: string[]
}

const base = '/api'

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${base}${path}`)
  if (!r.ok) throw new Error(`${path} -> ${r.status}`)
  return r.json() as Promise<T>
}

export const fetchHealth = () => get<{ status: string; engine: string }>('/health')
export const fetchModules = () => get<ModuleSummary[]>('/modules')
export const fetchManifest = (id: string, version: string) =>
  get<Record<string, unknown>>(`/modules/${id}/${version}`)
