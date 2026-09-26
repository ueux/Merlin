import StageStepper from '../components/StageStepper'

const DOMAINS = [
  { label: 'Mechanical', value: 100 },
  { label: 'Electronics', value: 96 },
  { label: 'Software', value: 100 },
  { label: 'Simulation', value: 91 },
  { label: 'Docs', value: 88 },
]

const MODULES = [
  { name: 'Drive Base', version: 'v2.1', status: 'ok' },
  { name: 'Arm', version: 'v4.2', status: 'ok' },
  { name: 'LiDAR', version: 'v3.1', status: 'ok' },
  { name: 'Battery', version: 'v2.0', status: 'warn' },
]

const ISSUES = [
  {
    check: 'bus_config',
    text: 'CAN node on CAN-FD bus — relaxed to CAN 2.0 framing at 1 Mbit; FD throughput unavailable',
  },
  {
    check: 'power_budget',
    text: 'Connector mismatch: battery provides XT60, actuator expects XT30 — adapter required',
  },
]

const ACTIVITY = [
  { hash: 'a83fd21', msg: 'fix: raise CAN-FD baud to 5Mbit for hip chain', when: '2h ago' },
  { hash: 'f42c9e0', msg: 'chore: regenerate glTF derivatives for leg_lower', when: '5h ago' },
  { hash: '91bd77a', msg: 'docs: update battery harness pinout', when: '1d ago' },
]

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-[10px] border border-border bg-panel p-4">
      <h2 className="mb-3 font-mono text-[10px] tracking-wider text-text-3 uppercase">{title}</h2>
      {children}
    </section>
  )
}

function Donut({ value }: { value: number }) {
  const r = 52
  const c = 2 * Math.PI * r
  return (
    <div className="relative h-32 w-32">
      <svg viewBox="0 0 120 120" className="h-full w-full -rotate-90">
        <circle cx="60" cy="60" r={r} fill="none" stroke="#111a2a" strokeWidth="10" />
        <circle
          cx="60"
          cy="60"
          r={r}
          fill="none"
          stroke="#22c55e"
          strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={c * (1 - value / 100)}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-2xl font-semibold">{value}%</span>
        <span className="font-mono text-[10px] text-ok">HEALTHY</span>
      </div>
    </div>
  )
}

export default function Overview() {
  return (
    <div className="space-y-4 p-6">
      <div className="flex items-center gap-3">
        <h1 className="text-lg font-semibold">Atlas Rover</h1>
        <span className="rounded-full border border-ok/40 bg-ok/10 px-2.5 py-0.5 font-mono text-[10px] text-ok">
          HEALTHY
        </span>
        <span className="font-mono text-[11px] text-text-3">v2.3.1 · main @ a83fd21</span>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <Card title="Robot Health">
          <div className="flex items-center justify-center py-2">
            <Donut value={94} />
          </div>
        </Card>

        <Card title="Domain Health">
          <div className="space-y-2.5 py-1">
            {DOMAINS.map((d) => (
              <div key={d.label} className="flex items-center gap-3">
                <span className="w-24 text-[12px] text-text-2">{d.label}</span>
                <div className="h-1.5 flex-1 rounded-full bg-panel-2">
                  <div
                    className={`h-1.5 rounded-full ${d.value >= 95 ? 'bg-ok' : 'bg-warn'}`}
                    style={{ width: `${d.value}%` }}
                  />
                </div>
                <span className="w-8 text-right font-mono text-[11px] text-text-2">{d.value}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card title="Pipeline">
          <div className="flex items-center justify-center py-4">
            <StageStepper current={2} />
          </div>
          <p className="text-center font-mono text-[11px] text-text-3">
            Simulate in progress · 100 scen / 40 batt / 20 therm
          </p>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card title="Modules">
          <ul className="divide-y divide-border">
            {MODULES.map((m) => (
              <li key={m.name} className="flex items-center gap-3 py-2">
                <span
                  className={`h-1.5 w-1.5 rounded-full ${m.status === 'ok' ? 'bg-ok' : 'bg-warn'}`}
                />
                <span className="text-[13px]">{m.name}</span>
                <span className="ml-auto font-mono text-[11px] text-text-2">{m.version}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Flagged Issues">
          <ul className="space-y-2">
            {ISSUES.map((issue) => (
              <li
                key={issue.check}
                className="rounded-md border border-warn/30 bg-warn/5 px-3 py-2"
              >
                <span className="font-mono text-[10px] text-warn">{issue.check}</span>
                <p className="mt-0.5 text-[12px] text-text-2">{issue.text}</p>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <Card title="Recent Activity">
          <ul className="divide-y divide-border">
            {ACTIVITY.map((a) => (
              <li key={a.hash} className="flex items-center gap-3 py-2">
                <span className="font-mono text-[11px] text-info">{a.hash}</span>
                <span className="truncate text-[12px] text-text-2">{a.msg}</span>
                <span className="ml-auto shrink-0 font-mono text-[10px] text-text-3">{a.when}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Simulation">
          <div className="flex items-center justify-between py-1">
            <div>
              <div className="text-[13px]">Run #248 — profile full</div>
              <div className="mt-1 font-mono text-[11px] text-text-3">
                pass rate 91% · Gazebo Harmonic / DART
              </div>
            </div>
            <span className="rounded-full border border-border px-2.5 py-1 font-mono text-[10px] text-text-2">
              UNITY HIL OFFLINE
            </span>
          </div>
        </Card>
      </div>
    </div>
  )
}
