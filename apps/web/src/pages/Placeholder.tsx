export default function Placeholder({
  title,
  milestone,
  note,
}: {
  title: string
  milestone: string
  note: string
}) {
  return (
    <div className="flex h-full items-center justify-center p-6">
      <div className="w-full max-w-md rounded-[10px] border border-border bg-panel p-8 text-center">
        <div className="font-mono text-[11px] text-accent">{milestone}</div>
        <h1 className="mt-2 text-xl font-semibold">{title}</h1>
        <p className="mt-2 text-[13px] text-text-2">{note}</p>
        <p className="mt-5 border-t border-border pt-4 font-mono text-[10px] text-text-3">
          SPEC: Frontend-Design.md · REFERENCE: stitch_merlin_robot_engineering_platform
        </p>
      </div>
    </div>
  )
}
