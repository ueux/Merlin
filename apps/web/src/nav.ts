export interface NavItem {
  path: string
  label: string
  icon: string
  section: string
  community?: boolean
}

export const NAV: NavItem[] = [
  { path: '/', label: 'Overview', icon: 'dashboard', section: 'Build' },
  { path: '/builder', label: 'Module Builder', icon: 'precision_manufacturing', section: 'Build' },
  { path: '/robots', label: 'Robots', icon: 'smart_toy', section: 'Build' },
  { path: '/registry', label: 'Module Registry', icon: 'inventory_2', section: 'Build' },
  { path: '/mechanical', label: 'Mechanical', icon: 'architecture', section: 'Engineering' },
  { path: '/electronics', label: 'Electronics', icon: 'memory', section: 'Engineering' },
  { path: '/software', label: 'Software', icon: 'code', section: 'Engineering' },
  { path: '/simulation', label: 'Simulation', icon: 'science', section: 'Engineering' },
  { path: '/tests', label: 'Tests', icon: 'checklist', section: 'Verify' },
  { path: '/releases', label: 'Releases', icon: 'rocket_launch', section: 'Verify' },
  { path: '/marketplace', label: 'Marketplace', icon: 'storefront', section: 'Community' },
  { path: '/open-source', label: 'Open Source', icon: 'public', section: 'Community', community: true },
]

export const PLACEHOLDERS: Record<string, { milestone: string; note: string }> = {
  builder: { milestone: 'M2', note: 'Drag-and-drop composition canvas with live engine validation on every drop.' },
  robots: { milestone: 'M2', note: 'Robot gallery: every robot, its pipeline state, and per-domain tool status.' },
  mechanical: { milestone: 'M3', note: 'SolidWorks vault sync, STEP/glTF derivatives, version compare views.' },
  electronics: { milestone: 'M3', note: 'Altium 365 sync, DRC status, BOM health, power budget rollups.' },
  software: { milestone: 'M2', note: 'ROS 2 packages, build farm status, ros2_control hardware graphs.' },
  simulation: { milestone: 'M4', note: 'Gazebo runs, scenario profiles, Foxglove live streams, HIL workers.' },
  tests: { milestone: 'M4', note: 'SIL/HIL suites, flaky-test tracking, trend sparklines.' },
  releases: { milestone: 'M5', note: 'Versioned machine manifests with full artifact sets and publish gates.' },
  marketplace: { milestone: 'M6', note: 'Verified-compatible parts with the compatibility guarantee.' },
  'open-source': { milestone: 'M6', note: 'Community machine manifests, clones, and contributors.' },
}
