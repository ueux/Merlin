import { NavLink } from 'react-router-dom'
import { NAV } from '../nav'

const SECTIONS = ['Build', 'Engineering', 'Verify', 'Community']

export default function Sidebar() {
  return (
    <aside className="flex w-56 shrink-0 flex-col border-r border-border bg-panel">
      <div className="border-b border-border px-4 py-4">
        <div className="text-[15px] font-semibold tracking-wide">MERLIN</div>
        <div className="mt-0.5 font-mono text-[10px] tracking-wider text-text-3">
          ROBOT LIFECYCLE PLATFORM
        </div>
      </div>
      <nav className="flex-1 space-y-4 overflow-y-auto px-2 py-3">
        {SECTIONS.map((section) => (
          <div key={section}>
            <div className="px-3 pb-1 font-mono text-[10px] tracking-wider text-text-3 uppercase">
              {section}
            </div>
            {NAV.filter((i) => i.section === section).map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `relative flex items-center gap-2.5 rounded-md px-3 py-1.5 text-[13px] transition-colors ${
                    isActive
                      ? item.community
                        ? 'bg-panel-2 font-medium text-community'
                        : 'bg-panel-2 font-medium text-text'
                      : 'text-text-2 hover:bg-panel-2/60 hover:text-text'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {isActive && (
                      <span
                        className={`absolute left-0 h-4 w-0.5 rounded ${
                          item.community ? 'bg-community' : 'bg-accent'
                        }`}
                      />
                    )}
                    <span className="material-symbols-outlined !text-[18px]">{item.icon}</span>
                    {item.label}
                  </>
                )}
              </NavLink>
            ))}
          </div>
        ))}
      </nav>
      <div className="border-t border-border px-4 py-3 font-mono text-[10px] text-text-3">
        engine v0.1.0 · schema 1.0.0
      </div>
    </aside>
  )
}
