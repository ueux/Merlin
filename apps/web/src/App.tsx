import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import { NAV, PLACEHOLDERS } from './nav'
import Overview from './pages/Overview'
import Placeholder from './pages/Placeholder'
import Registry from './pages/Registry'

const IMPLEMENTED = new Set(['/', '/registry'])

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Overview />} />
          <Route path="registry" element={<Registry />} />
          {NAV.filter((i) => !IMPLEMENTED.has(i.path)).map((item) => {
            const key = item.path.slice(1)
            const meta = PLACEHOLDERS[key] ?? { milestone: 'M?', note: '' }
            return (
              <Route
                key={item.path}
                path={key}
                element={<Placeholder title={item.label} milestone={meta.milestone} note={meta.note} />}
              />
            )
          })}
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
