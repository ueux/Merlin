# RoboForge — Frontend Design Breakdown

> Reverse-engineered from the two reference mockups (Robot Overview dashboard + Module Builder workspace).
> Purpose: turn the mockups into an implementable frontend specification — tokens, shell, IA, screens, components, states, and data binding to the three schemas (`robot-manifest`, `module-manifest`, `composition`).

---

## 1. Design Language

The mockups use a **dark, dense, IDE-grade aesthetic** — visually "Linear × GitHub × CAD workstation". This is the right register for a developer/engineering tool: it signals precision, keeps 3D content legible, and lets status colors carry meaning.

| Trait | Choice in mockups | Rationale |
|---|---|---|
| Theme | Dark-only, near-black navy | 3D viewport contrast; long-session eye strain; "engineering console" feel |
| Density | High (12–13px body, tight padding) | Expert users, lots of telemetry on one screen |
| Depth | Flat panels + 1px borders, no heavy shadows | Separation via border + background step, not elevation |
| Accent | Single saturated blue for primary actions | One "where do I click" answer per screen |
| Status colors | Green/amber/red + cyan info, used consistently | Health, validation, pipeline state readable at a glance |
| Brand moments | Gradient donut gauge, gradient logo mark, purple open-source banner | Sparingly used gradients keep the UI from feeling sterile |

---

## 2. Design Tokens

Extracted from the mockups (approximate hex values; to be locked when the token file is authored).

### 2.1 Color

```
--bg-app:        #070B14   /* page background */
--bg-panel:      #0D1420   /* cards / panels */
--bg-panel-2:    #111A2A   /* nested panels, hover */
--bg-input:      #0A111D
--border:        #1C2740   /* 1px panel borders */
--border-strong: #2A3A5C

--text-primary:  #F1F5F9
--text-secondary:#8FA1BC
--text-muted:    #5B6B87

--accent:        #2E7CF6   /* primary buttons, active tab, links */
--accent-hover:  #4A8DF8
--accent-soft:   rgba(46,124,246,.14)

--success:       #22C55E
--warning:       #F59E0B
--danger:        #EF4444
--info:          #06B6D4
--purple:        #8B5CF6   /* open-source / community only */

--gauge-gradient: linear-gradient(135deg,#22C55E,#06B6D4)
```

**Semantic rule:** green/amber/red are *reserved* for status (never decoration). Purple is reserved for community/open-source surfaces. Blue is reserved for actions.

### 2.2 Typography

| Token | Value | Usage |
|---|---|---|
| `font-sans` | Inter (fallback: system-ui) | everything |
| `font-mono` | JetBrains Mono | commit hashes (`a83fd21`), versions, file paths, code |
| `text-xs` | 11–12px | badges, table meta, timeline timestamps |
| `text-sm` | 12.5–13px | body, lists, panel content |
| `text-md` | 14–15px | panel titles, nav items |
| `text-lg` | 17–18px semibold | section headers ("Atlas Rover") |
| `text-xl` | 22–24px semibold | page-level numbers (94%) |

### 2.3 Shape & spacing

- Radius: `--r-sm 6px` (badges, chips), `--r-md 10px` (cards), `--r-pill 999px` (status pills, stepper nodes)
- Border: 1px `--border` on every panel; panels sit on `--bg-app` with an 8–12px gap
- Spacing scale: 4px base (4/8/12/16/24/32)
- Icon size: 16px nav, 14px inline, 18px rail

### 2.4 Iconography

Line icons, 1.5px stroke (Lucide-style). Domain glyphs are consistent across both mockups: cube = mechanical/module, chip = electronics, `</>` = software, flask = material test, play = simulation, gauge = health, branch = git.

---

## 3. Application Shell

Both screens share one shell with **three persistent regions**:

```
┌────────────────────────────────────────────────────────────────┐
│ TopBar  (logo · context tabs · ⌘K search · alerts · user)      │ 48px
├──────────┬─────────────────────────────────────────────────────┤
│          │  Robot Header (identity · version · pipeline · CTA) │ ~96px (project scope only)
│ Sidebar  ├─────────────────────────────────────────────────────┤
│  240px   │                                                     │
│ (grouped │              Screen content (per-route grid)        │
│   nav)   │                                                     │
│          │                                                     │
├──────────┴─────────────────────────────────────────────────────┤
│ Plan widget (Free Plan 3/5 robots · storage · Upgrade)         │ sidebar footer
└────────────────────────────────────────────────────────────────┘
```

### 3.1 TopBar
- **Left:** logo; in project scope it gains context tabs (`Design · Build · Test · Open Source`) — these are the four product "modes".
- **Center:** global search / **command palette** (`⌘K`) — "Search robots, modules, files, or commands". This is the primary power-user feature and must search *across* artifact types (robot, module, file, commit, command).
- **Right:** notifications, presence/collaborators (avatar stack "+3" in project scope), user menu.

### 3.2 Sidebar — two nav modes
The mockups show the shell in **two scopes**, and the sidebar changes with scope:

**Global scope (Image 1)** — cross-project navigation:
`Home, Overview` · `ROBOT: Robots, Modules, Marketplace, Open Source` · `SIMULATION: Environments, Simulation, Digital Twin` · `VALIDATION: Tests, Results, Hardware` · `ECOSYSTEM: Community, Documentation` · `PROJECT: Releases, Activity, Settings`

**Project scope (Image 2)** — inside one robot (`Atlas Rover`), with the robot switcher + branch at top and artifact-type entries carrying integration badges (`Mechanical · SolidWorks`, `Electronics · Altium`):
`Overview, Robot, Mechanical, Electronics, Materials & Tests, Software, Simulation, Environments ▸ (ROS 2, RViz, Gazebo, MoveIt, Unity, Isaac Sim), Modules, Marketplace, Releases`
Footer: **Project Stats** (Files 248 · Commits 42 · Branches 6 · Last Updated 2h ago).

### 3.3 Robot Header (project scope)
Identity block (thumbnail, name, `Healthy` badge, one-line description) + version row (`v2.3.1` · branch `main` · "Updated 2 hours ago") + long description + primary CTA **`Run Simulation ▾`** (split button with dropdown for env/profile choice) + overflow menu.

### 3.4 Pipeline Stepper
Persistent 5-stage lifecycle indicator, directly under the header on both screens:

`Design → Integrate → Simulate → Validate → Release`

Node states: **completed** (green ✓), **in-progress** (blue ▶), **pending** (gray). This is the platform's core mental model made visible — every robot is always *somewhere* in this pipeline. Driven by manifest system status + test/validation aggregation (see §7).

---

## 4. Information Architecture & Routes

```
/                              → Home (global dashboard)
/robots                        → robot list (grid/table, health filter)
/robots/:robotId               → Overview            [SCREEN 1]
/robots/:robotId/design        → Module Builder      [SCREEN 2]  (mode: Design)
/robots/:robotId/mechanical    → CAD artifacts (SolidWorks) — versions, derivatives, viewer
/robots/:robotId/electronics   → EDA artifacts (Altium) — schematics, PCB, BOM
/robots/:robotId/materials     → materials & test specimens/results
/robots/:robotId/software      → repos, packages, builds, commits
/robots/:robotId/simulation    → sim sessions/profiles           (mode: Test)
/robots/:robotId/environments  → env fleet status (Gazebo/RViz/MoveIt/Unity/Isaac)
/robots/:robotId/tests         → test suites & runs
/robots/:robotId/releases      → versioned releases
/robots/:robotId/activity      → full timeline
/modules                       → module registry (our manifests)
/marketplace                   → paid/shared modules & robots
/open-source                   → public robot space               (mode: Open Source)
/community, /docs              → ecosystem
/settings                      → org/project settings
```

Only the two mockup screens are specified in detail below; the rest are implied routes for the IA to be complete.

---

## 5. Screen 1 — Robot Overview (`/robots/:id`)

**Job:** answer four questions in 5 seconds — *What is this robot? Is it healthy? What changed? What can I do next?*

### 5.1 Layout grid

```
┌───────────────┬─────────────────────────────┬────────────────┐
│ Robot State   │                             │ Robot Health   │
│ (versions per │      3D Viewport            │  (94% donut +  │
│  domain)      │  tabs: 3D/Exploded/         │   per-domain %)│
│               │       Components/Dimensions │                │
│ Quick Actions │                             │ Recent Issues  │
│               │                             │                │
│               │                             │ Activity       │
│               │                             │ Timeline       │
├───────────────┴──────────────┬──────────────┴────────────────┤
│ Key Components (module cards)│ Simulation Environments       │
├──────────────────────────────┴───────────────────────────────┤
│ Open Source banner → Explore Community                       │
└──────────────────────────────────────────────────────────────┘
   col 1: ~300px fixed   col 2: fluid (min 480px)   col 3: ~320px fixed
```

### 5.2 Panel inventory

| # | Panel | Contents | Interactions | Data source |
|---|---|---|---|---|
| 1 | **Robot State** | `Validated` pill; per-domain rows: Mechanical `v3.2` ✓, Electronics `v1.4` ✓, Software `a83fd21` ✓, Simulation `pending`, Tests `pending` | Row click → domain page; "View Details →" | robot-manifest `systems.*` versions + aggregated status |
| 2 | **Quick Actions** | Run Simulation (primary), Open in RViz, View Source, View Documentation | Buttons; RViz opens embedded viewer | static + env availability |
| 3 | **3D Viewport** | Tabs: `3D View / Exploded View / Components / Dimensions`; left tool rail (select, camera, orbit, fullscreen); gizmo axes; bottom-right view controls | Orbit/zoom/pan; exploded slider; component isolation; dimension overlay | glTF **derivative** of mechanical CAD (native+derivatives pattern) |
| 4 | **Robot Health** | 94% gradient donut; per-domain %: Mechanical 100, Electrical 96, Software 100, Simulation 91, Testing 88 | Hover → what drags the score | computed from validation checks + test runs |
| 5 | **Recent Issues** | Iconed list: "Battery test not completed · 2d", "CAD revision differs from simulation · 3d", "Firmware dependency not verified · 5d"; View All | Click → issue detail/ filtered tests | composition `validation.errors/warnings` + test gaps |
| 6 | **Activity Timeline** | Vertical feed: SolidWorks v3.2 update, Gazebo build (100 scenarios), Altium v1.4 release, ROS build passed `@a83fd21`, material test uploaded (Aluminium 6061) — each with domain icon + relative time | Filter by domain (future) | cross-domain event log (the `links[]` graph rendered as time) |
| 7 | **Key Components** | Module cards: Drive Base v2.1, Robotic Arm v4.2, LiDAR v3.1, Battery Pack v2.0 — each `Compatible` | Click → module inspector; View All | robot-manifest `modules[]` (moduleUse) → module registry |
| 8 | **Simulation Environments** | Env chips: Gazebo Ready, RViz Ready, MoveIt Ready, Isaac Sim Ready, Unity **Offline** | Click → env page; run | robot-manifest `simulation` + infra status |
| 9 | **Open Source banner** | "Share your robot with the community…" + Explore Community → | Route to publish flow | publication status |

### 5.3 UX notes
- The page is **read-mostly**: the only primary action is `Run Simulation`. Everything else is navigation into a domain.
- `pending` states (Simulation, Tests rows) are deliberate — the dashboard doubles as a **gap detector**: what's not validated yet is as visible as what is.
- Health gauge is a *summary*, not a metric to trust blindly — clicking it must reveal the breakdown/formula.

---

## 6. Screen 2 — Module Builder (`/robots/:id/design`)

**Job:** the flagship drag-and-drop modular composition flow — pick modules from a library, see them snap together in 3D, get *live* compatibility verdicts, commit the build.

This screen is the visual frontend of our **composition schema**; the left library is the **module registry**; the inspector is a rendered **module manifest**.

### 6.1 Layout

```
┌────┬──────────────┬──────────────────────────┬────────────────┐
│icon│ Module       │                          │ Selected       │
│rail│ Builder      │      3D Viewport         │ Component      │
│64px│ panel 320px  │  (canvas + view opts)    │ inspector 360px│
│    │              │                          │                │
├────┴──────────────┼──────────────┬───────────┴────────────────┤
│                   │ Timeline/    │ Build Graph │ Recent       │
│                   │ Tests donut  │   (DAG)     │ Commits      │
├───────────────────┴──────────────┴────────────────────────────┤
│ Simulation Environments strip          │ Quick Actions        │
└────────────────────────────────────────┴──────────────────────┘
```

### 6.2 Module Builder panel (left)

- **Tabs:** `Modules` (registry) · `My Build` (instances in current composition) · `Library` (org/saved).
- **Module cards grid** (2-col): thumbnail, name, category label — Drive Base (Mobility), Arm (Manipulator), Gripper (End Effector), LiDAR (Perception), Camera (Vision), Battery (Power), Compute (Processing), Motor Controller (Control). Each has a `+` to add.
  - Category labels map 1:1 to module-manifest `category` enum (actuator/link/sensor/power/controller/endeffector/structure/comms).
- **Module Compatibility graph:** live node graph of the current composition — nodes = instances (Battery, Compute, Drive Base, LiDAR, Camera, Arm, Gripper), edges colored by relationship type (power=green, data=blue, mechanical=amber).
- **Verdict line:** `✓ All selected modules are compatible` — the aggregate of the composition validation checks.
- **`Add to Robot`** primary button — commits the composition (writes a validated composition document + regenerates outputs).

### 6.3 3D Viewport (center)

- Same viewport component as Screen 1, in **edit mode**: drag a module card → drop near a highlighted compatible interface → snap preview (ghost + target interface highlight) → confirm mate.
- View options popover: `Grid / Floor / Axes / Shadows` checkboxes.
- Top-right toggles: 3D / explode / wireframe / fullscreen. Bottom-center: transform gizmo controls.
- Top tabs for the workspace: `3D View · Diagram · Assembly · Code` — Diagram = node graph view of the composition; Assembly = tree; Code = generated xacro (the composition `outputs.xacro`).

### 6.4 Selected Component inspector (right)

Rendered directly from a **module manifest** — shown: "Differential Drive Base", `Compatible` badge, `Mobility · Base` category.

Tabs: **Details · Dependencies · Versions**.

Details rows (manifest field in parens):
- Power Budget `24V 15A (360W)` (`electrical.power[]` + `compat.power_budget`)
- Mounting Interface `Standard M6 Pattern` (`mechanical.interfaces[].bolt_pattern`)
- Firmware `v1.2.3` (`software.drivers[]`)
- ROS 2 Package `diff_drive_base` (`software.ros2`/package ref)
- CAD Revision `v3.2.1` (`mechanical.assets`)
- PCB Revision `v1.4.0` (`electrical` assets)

**Compatibility checklist** — per-domain verdicts, each mapping to a composition validation check:
| Checklist row | Composition check |
|---|---|
| Power System ✓ | `power_budget` |
| Control System ✓ | `bus_config` |
| Mechanical Interface ✓ | `mate_matching` |
| Software Stack ✓ | `software_interfaces` |

### 6.5 Bottom strip

- **Timeline / Build Graph / Test Results / Logs** tabbed panel:
  - *Timeline:* today's events (SolidWorks update 10:24, Altium schematic 09:17, CI build #142 08:43, Gazebo test 07:12, unit tests 06:58).
  - *Test Results:* donut `12/12 · 100%` with per-suite rows (Unit 12/12, Integration 8/8, Simulation 6/6, Performance 4/4).
- **Build Graph** (DAG): `robot_description (URDF)` + `navigation2` + `perception` → `atlas_robot (workspace)` → `mechanical / electronics / software` — colcon build topology rendered as a graph; nodes carry pass/fail dots.
- **Recent Commits:** hash (mono font), message, author, relative time — git integration surfaced in-context.
- **Footer strip:** environment fleet status (`ROS 2 Running`, RViz/Gazebo/MoveIt/Unity/Isaac `Available`) + Quick Actions: **Export Robot**, **Publish Open Source**, **Create New Module**.

---

## 7. State & Status Vocabulary (UI ↔ schema enums)

Consistent enums across UI and schemas — the UI never invents states:

| UI element | Values | Source of truth |
|---|---|---|
| Pipeline stepper | completed / in-progress / pending | derived: which manifest sections are populated + validated |
| Domain row state | version + ✓ / pending | robot-manifest `systems.*` presence + validation |
| Health gauge | 0–100 aggregate | weighted validation + test pass rates |
| Module verdict | Compatible / Warning / Incompatible | composition `validation.checks[]` status (pass/warn/fail) |
| Composition status | valid / warnings / invalid | composition `validation.status` |
| Env status | Ready / Running / Available / Offline | infra probes + manifest `simulation.sim_profiles` |
| Test kind | unit / integration / sim / hil / field / performance | robot-manifest `testing.test_runs[].kind` |
| Issue severity | warning(amber) / error(red) | validation errors vs warnings |

---

## 8. Interaction Model

1. **Keyboard-first:** `⌘K` palette everywhere; `g then r` style nav (future); viewport hotkeys (orbit/pan/explode).
2. **Drag-and-drop composition:** module card → canvas = add instance; card → compatible interface = propose mate. Incompatible drop targets show red outline + reason tooltip (from the failing check).
3. **Live validation:** every composition mutation re-runs checks (debounced); the compatibility graph and verdict line update without a save step — the schema's authored-vs-computed split makes this natural (recompute computed sections, never hand-edit them).
4. **Split-button Run Simulation:** default profile = last used; dropdown picks env + world + scenario count.
5. **Progressive disclosure:** dashboards show verdicts; the *reason* is one click away (check details, logs).
6. **Everything is versioned and linkable:** every row (CAD v3.2, commit a83fd21, module v2.1) deep-links to its version page.

---

## 9. Component Inventory (build list)

**Primitives:** Button (primary/ghost/icon/split), Badge/StatusPill, Card/Panel, Tabs, SearchInput, CommandPalette (cmdk), Dropdown/Popover, Tooltip, CheckboxList, AvatarStack, ProgressRing, DonutGauge, Skeleton, EmptyState, Toast.

**Navigation:** Sidebar (scoped, grouped), IconRail, TopBar, RobotHeader, PipelineStepper, ProjectSwitcher (robot + branch), PlanWidget.

**Data display:** KeyValueList, VersionChip (mono), TimelineFeed, CommitList, IssueList, TestSummaryDonut, HealthGauge, StatRow, EnvStatusChip.

**Domain components:**
- `Viewport3D` — R3F canvas: glTF load, exploded slider, dimension overlay, component isolation, mate-highlight shaders, view-options store.
- `ModuleCard` / `ModuleLibraryGrid`
- `CompatibilityGraph` — nodes/edges typed by relation (power/data/mech), live verdict styling.
- `BuildGraph` — read-only DAG with pass/fail nodes.
- `ModuleInspector` — Details/Dependencies/Versions tabs (renders a module manifest).
- `MateProposalOverlay` — drop-target highlight + interface match preview.
- `RobotStatePanel`, `QuickActionsPanel`.

---

## 10. Tech Stack Recommendation

| Concern | Choice | Why |
|---|---|---|
| Framework | React 18 + TypeScript + Vite | fast dev, SPA shell; Next.js only for public marketplace/docs SEO pages |
| Styling | Tailwind + CSS-var tokens + shadcn/ui primitives | matches token table; speed |
| 3D | three.js via **react-three-fiber + drei** | glTF derivatives straight from the manifest pipeline |
| Graph views | **reactflow** | CompatibilityGraph + BuildGraph share one engine |
| ROS live viz | Foxglove (embedded) + rosbridge | matches research conclusion (Foxglove/MCAP) |
| Sim streaming | WebRTC/noVNC embed | headless Gazebo containers |
| Code | Monaco | xacro/URDF view + edit |
| State | Zustand (UI) + TanStack Query (server) | small, typed, cache-friendly |
| Validation | shared TS port of the Python validation engine + `ajv` for schemas | same rules client (instant) & server (authoritative) |
| Testing | Vitest + Playwright | component + e2e golden paths |

---

## 11. Gaps the mockups don't show (design later)

- Auth / org onboarding / robot creation wizard
- Module **publish** flow (authoring a manifest in UI)
- Simulation run **configuration** screen (world, scenarios, seeds)
- Version **diff** views (CAD rev vs sim — the exact issue in Recent Issues)
- Sharing/permissions UI, marketplace purchase flow
- Mobile/responsive story — these are desktop workstation layouts; below ~1280px the three-column grids need a defined collapse order (inspector → overlay drawer, bottom strip → tab)

---

## 12. Build Phasing (mapped to roadmap)

| Phase | Frontend scope |
|---|---|
| M1 Core | Shell, global nav, /robots list, Overview read-only (panels 1,4,6,7), tokens |
| M2 Software | Timeline, Commits, Build Graph, Test donut |
| M3 Builder | Module Builder full: library grid, drag-drop, CompatibilityGraph, inspector, live validation |
| M4/M5 Mech/Elec | Viewport3D derivatives, CAD/EDA pages, version diffs |
| M7 Simulation | Run Simulation flow, env strip, Foxglove/noVNC embeds |
| M8 Publishing | Open Source banner flow, marketplace, community |
