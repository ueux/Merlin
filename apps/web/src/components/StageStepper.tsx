const STAGES = ['Design', 'Integrate', 'Simulate', 'Validate', 'Release']

export default function StageStepper({ current }: { current: number }) {
  return (
    <ol className="flex items-start">
      {STAGES.map((stage, i) => (
        <li key={stage} className="flex items-start">
          <div className="flex flex-col items-center gap-1.5">
            <span
              className={`flex h-6 w-6 items-center justify-center rounded-full border font-mono text-[11px] ${
                i < current
                  ? 'border-ok bg-ok/15 text-ok'
                  : i === current
                    ? 'border-accent bg-accent/15 text-accent'
                    : 'border-border text-text-3'
              }`}
            >
              {i < current ? '✓' : i + 1}
            </span>
            <span className={`text-[11px] ${i <= current ? 'text-text' : 'text-text-3'}`}>
              {stage}
            </span>
          </div>
          {i < STAGES.length - 1 && (
            <span className={`mx-2 mt-3 h-px w-10 ${i < current ? 'bg-ok' : 'bg-border'}`} />
          )}
        </li>
      ))}
    </ol>
  )
}
