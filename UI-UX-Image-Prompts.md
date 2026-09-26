# MERLIN — UI/UX Image Generation Prompts

> Purpose: generate consistent, high-fidelity UI reference images for every core screen of the MERLIN platform (robot lifecycle IDE). Every prompt is grounded in `Frontend-Design.md` — same tokens, same layouts, same data.
> Usage: paste the **MASTER STYLE BLOCK** + one **SCREEN BLOCK** into your image generator (Midjourney, DALL·E 3, SDXL, Firefly). Do not reorder; the style block must come first.

---

## 1. Global generation settings

| Setting | Value |
|---|---|
| Aspect ratio | **16:9** (1792×1024 or 1920×1080) — desktop workstation app |
| Style keywords | `high-fidelity desktop web application UI mockup, product design screenshot, Figma/Linear-style interface, dark mode, crisp vector-sharp panels, realistic UI typography` |
| Avoid (negative prompt) | `photo of a screen, laptop mockup, perspective tilt, blurry text, lorem ipsum, mobile app, light theme, 3D render of a room, people, hands, watermark` |
| Text note | Generators garble small text — treat labels as indicative; regenerate rather than upscale. If a tool supports it, generate at max resolution. |

**Canonical demo data** (reuse across ALL screens for consistency):
- Robot: **Atlas Rover**, `Healthy`, version `v2.3.1`, branch `main`, commit `a83fd21`
- Pipeline: `Design ✓ → Integrate ✓ → Simulate ▶ → Validate → Release`
- Health: **94%** (Mechanical 100 · Electrical 96 · Software 100 · Simulation 91 · Testing 88)
- Modules: Drive Base v2.1 · Robotic Arm v4.2 · LiDAR v3.1 · Battery Pack v2.0
- Envs: Gazebo/RViz/MoveIt/Isaac Sim **Ready**, Unity **Offline**
- Tests: `12/12 · 100%` (Unit 12/12, Integration 8/8, Simulation 6/6, Performance 4/4)
- Stats: Files 248 · Commits 42 · Branches 6 · Updated 2h ago

---

## 2. MASTER STYLE BLOCK (prepend to every prompt)

```
High-fidelity desktop web application UI mockup for "MERLIN", a dark-mode robot
engineering platform (visual register: Linear × GitHub × CAD workstation console).
Flat 2D interface, front view, full-screen browser window, no device frame.

Design system, apply exactly:
- Page background near-black navy #070B14; panels #0D1420 with 1px borders #1C2740,
  10px corner radius, no drop shadows; nested panels #111A2A.
- Text: Inter font family; primary #F1F5F9, secondary #8FA1BC, muted #5B6B87;
  code/versions/commit hashes in JetBrains Mono.
- Single saturated blue accent #2E7CF6 reserved for primary actions, active tabs
  and links only.
- Status colors used ONLY for status: green #22C55E (pass/healthy), amber #F59E0B
  (warning), red #EF4444 (error), cyan #06B6D4 (info). Purple #8B5CF6 reserved for
  open-source/community surfaces only.
- High information density: 12–13px body text, tight 8–12px padding, 1.5px-stroke
  line icons (Lucide style). Pills/badges fully rounded.
- Persistent shell on every screen: 48px top bar with hexagonal-circuit logo mark,
  centered ⌘K command-palette search pill ("Search robots, modules, files, or
  commands"), notification bell, stacked collaborator avatars "+3", user avatar.
  240px left sidebar with grouped navigation in muted caps section labels.
```

---

## 3. Screen prompts

### SCREEN 1 — Robot Overview dashboard (`/robots/:id`)

```
Screen: the Robot Overview dashboard for a robot called "Atlas Rover".

Sidebar (project scope): robot switcher "Atlas Rover · main" at top; nav items
with small line icons — Overview (active, blue), Robot, Mechanical (SolidWorks
badge), Electronics (Altium badge), Materials & Tests, Software, Simulation,
Environments (expandable: ROS 2, RViz, Gazebo, MoveIt, Unity, Isaac Sim),
Modules, Marketplace, Releases. Sidebar footer: "Project Stats — Files 248 ·
Commits 42 · Branches 6 · Last Updated 2h ago" and a small Free Plan widget
(3/5 robots, storage bar, Upgrade link).

Under the top bar, a robot header row: square thumbnail of an orange-and-grey
quadruped rover robot, title "Atlas Rover" with a green "Healthy" pill, one-line
description "Four-legged research rover for rough-terrain autonomy", version row
"v2.3.1 · branch main · Updated 2 hours ago", and a blue split button
"Run Simulation ▾". Directly below, a horizontal 5-stage pipeline stepper with
pill nodes: Design (green ✓) → Integrate (green ✓) → Simulate (blue ▶
in-progress) → Validate (grey) → Release (grey).

Three-column content grid (300px / fluid / 320px):
LEFT: "Robot State" panel — green "Validated" pill; rows: Mechanical v3.2 ✓
green, Electronics v1.4 ✓ green, Software a83fd21 (mono font) ✓ green,
Simulation "pending" grey, Tests "pending" grey. Below it a "Quick Actions"
panel: primary blue "Run Simulation" button, ghost buttons "Open in RViz",
"View Source", "View Documentation".
CENTER: large 3D viewport panel showing a rendered quadruped rover robot (grey
carbon-fiber legs, orange actuator housings) on a dark grid floor with a red/
green/blue axis gizmo; top tabs "3D View · Exploded View · Components ·
Dimensions"; slim left icon tool rail; small view controls bottom-right.
RIGHT: "Robot Health" panel with a large circular donut gauge "94%" stroked in a
green-to-cyan gradient, under it per-domain percentage bars (Mechanical 100,
Electrical 96, Software 100, Simulation 91, Testing 88); below, "Recent Issues"
list with amber/red icons — "Battery test not completed · 2d" (amber), "CAD
revision differs from simulation · 3d" (amber), "Firmware dependency not
verified · 5d" (red); below, "Activity" vertical timeline with domain icons:
SolidWorks v3.2 update, Gazebo build 100 scenarios, Altium v1.4 release, ROS
build passed @a83fd21, material test uploaded (Aluminium 6061).

Bottom rows: "Key Components" panel with four module cards (Drive Base v2.1,
Robotic Arm v4.2, LiDAR v3.1, Battery Pack v2.0) each with a green "Compatible"
pill; "Simulation Environments" panel with status chips — Gazebo Ready (green),
RViz Ready (green), MoveIt Ready (green), Isaac Sim Ready (green), Unity Offline
(grey). Full-width purple-accent banner: "Share your robot with the community —
publish it open source" with an "Explore Community →" button.
```

### SCREEN 2 — Module Builder (`/robots/:id/design`) — flagship

```
Screen: the Module Builder workspace (drag-and-drop modular robot composition).

Far left: slim 64px icon rail replacing the full sidebar (icons: home, cube,
chip, code, flask, play, settings). Next, a 320px "Module Builder" panel: tabs
"Modules · My Build · Library"; a 2-column grid of small module cards, each with
a simple robot-part thumbnail, name, category label and a "+" button — Drive
Base (Mobility), Arm (Manipulator), Gripper (End Effector), LiDAR (Perception),
Camera (Vision), Battery (Power), Compute (Processing), Motor Controller
(Control). Below the grid, a "Module Compatibility" node graph: small rounded
nodes (Battery, Compute, Drive Base, LiDAR, Camera, Arm, Gripper) connected by
colored edges — green edges for power, blue for data, amber for mechanical.
Under it a green verdict line "✓ All selected modules are compatible" and a
full-width blue "Add to Robot" button.

Center: large 3D viewport in edit mode showing a partially assembled robot —
differential drive base with two wheels, a mounted robotic arm, a LiDAR puck on
a mast — on a dark grid floor; a ghosted semi-transparent gripper module
snapping onto the arm tip with a highlighted amber mounting flange ring (mate
preview). Workspace top tabs: "3D View · Diagram · Assembly · Code". Top-right
viewport toggles: 3D, explode, wireframe, fullscreen; bottom-center transform
gizmo control.

Right: 360px "Selected Component" inspector for "Differential Drive Base" with a
green "Compatible" badge and "Mobility · Base" category; tabs "Details ·
Dependencies · Versions". Key-value rows: Power Budget "24V 15A (360W)",
Mounting Interface "Standard M6 Pattern", Firmware "v1.2.3", ROS 2 Package
"diff_drive_base" (mono), CAD Revision "v3.2.1", PCB Revision "v1.4.0". Below, a
"Compatibility" checklist with green checks: Power System ✓, Control System ✓,
Mechanical Interface ✓, Software Stack ✓.

Bottom strip: tabbed panel "Timeline · Build Graph · Test Results · Logs" —
Timeline tab active showing today's events with timestamps (SolidWorks update
10:24, Altium schematic 09:17, CI build #142 08:43, Gazebo test 07:12, unit
tests 06:58); beside it a test-results donut "12/12 · 100%" with suite rows
(Unit 12/12, Integration 8/8, Simulation 6/6, Performance 4/4); beside it a
"Recent Commits" list (mono hashes a83fd21, f42c9e0, 91bd77a with one-line
messages, authors, relative times). Footer strip: environment status chips
(ROS 2 Running green; RViz, Gazebo, MoveIt, Unity, Isaac Sim Available grey) and
Quick Actions: "Export Robot", "Publish Open Source", "Create New Module".
```

### SCREEN 3 — Module Builder: incompatibility state (validation warning)

```
Same Module Builder workspace layout as the flagship screen, but showing a
FAILED compatibility scenario for the "Atlas Rover" build:

The user has dragged a 48V Battery Pack module near the chassis; the drop target
mount outline glows RED with a tooltip "Incompatible: bolt pattern mismatch —
4xM4 on 60x40 grid vs 4xM4 on 30x30 grid". In the Module Compatibility graph,
the Battery node and its power edge to the Compute node are amber/red; the
verdict line reads "⚠ 2 warnings, 1 error — build cannot be committed" in amber,
and the "Add to Robot" button is disabled (grey).

Right inspector shows the Battery Pack with a red "Incompatible" badge; the
Compatibility checklist now reads: Power System ⚠ (amber, "CAN bus protocol
mismatch: battery BMS speaks classic CAN 1 Mbit/s, actuator expects CAN-FD
5 Mbit/s"), Control System ⚠ (amber), Mechanical Interface ✗ (red, "bolt
pattern mismatch on iface-mount"), Software Stack ✓ (green). A red-bordered
banner at the top of the inspector: "Fix 3 issues to commit this build".
The validation panel under the graph lists three rows with severity icons:
ERROR "bolt pattern mismatch (mate_matching)" red, WARNING "protocol mismatch
CAN vs CAN-FD (bus_config)" amber, WARNING "connector mismatch XT60 → XT30,
adapter required (power_budget)" amber.
```

### SCREEN 4 — Robots list (`/robots`, global scope)

```
Screen: global "Robots" gallery page. Sidebar shows GLOBAL navigation instead of
project nav: Home, Overview; section ROBOT: Robots (active), Modules,
Marketplace, Open Source; section SIMULATION: Environments, Simulation, Digital
Twin; section VALIDATION: Tests, Results, Hardware; section ECOSYSTEM:
Community, Documentation; section PROJECT: Releases, Activity, Settings.

Content header: "Robots" title, filter pills (All · Healthy · Attention ·
Archived), a view toggle (grid/table) and a blue "New Robot" button. A grid of
six robot cards (3 columns × 2 rows): each card has a 16:9 rendered thumbnail of
a different robot (quadruped rover, 6-axis arm on a mobile base, drone, tracked
UGV, biped leg test-rig, delta picker), robot name, one-line description, a
status pill (green "Healthy" ×4, amber "Attention" — "Atlas Arm: 3 open issues",
grey "Draft"), version + branch in mono ("v2.3.1 · main"), tiny domain icons row
(CAD, PCB, code, sim) with green/grey dots showing which domains are populated,
and a mini 5-dot pipeline progress indicator under each (first card: 2 green
dots + 1 blue + 2 grey). Card hover state on the first card: slightly lifted
border in stronger blue-grey #2A3A5C.
```

### SCREEN 5 — Module Registry (`/modules`)

```
Screen: the "Module Registry" — a package-registry browser (npm-for-robot-
modules feel). Header: "Module Registry" with search input "Search 128
modules…", category filter chips (All, Actuator, Link, Sensor, Power,
Controller, End Effector, Structure, Comms) and a blue "Publish Module" button.

Two-pane layout: LEFT (fluid) a table/list of module rows: small thumbnail,
name "ODRI 60 mm Actuator" with vendor "@open-dynamic-robot-initiative",
category pill "actuator", short description "Torque-controlled brushless
actuator, 9:1 planetary, CAN-FD daisy chain", version "v1.2.0" mono, hardware
license pill "BSD-3-Clause", download count, updated time; rows for
odri-actuator-60, tube-link-300, battery-pack-48v (CERN-OHL-P-2.0 license pill),
chassis-plate, cubemars-ak60-6, moteus-r4, realsense-d435 mount, bno085-imu.
RIGHT (360px) a detail pane for the selected row "odri-actuator-60": version
selector "1.2.0 ▾", README-style description, spec key-values (Mass 0.48 kg,
Nominal 24V, Peak 4A, Effort limit 6 N·m, Interface 6xM3 on 25 mm PCD flange),
"Compatible with" tag chips (pattern:6xM3_on_25mm_PCD, flange:pilot8), tabs
"Manifest · Interfaces · Versions" with the Manifest tab showing a syntax-
highlighted JSON snippet of the module manifest (dark code block, mono font,
blue keys / green strings). Bottom of pane: blue "Add to Build" button and ghost
"View Source".
```

### SCREEN 6 — Mechanical page (`/robots/:id/mechanical`)

```
Screen: the Mechanical (CAD) artifacts page for Atlas Rover, project-scope
sidebar with "Mechanical" active and its SolidWorks integration badge.

Header row: "Mechanical" title, green pill "SolidWorks connected · vault
synced", branch "main", blue button "Open in SolidWorks". Sub-tabs: "Files ·
Versions · Derivatives · Diff".

Content: LEFT (fluid) a file table of CAD artifacts: icon, filename
(chassis_top.SLDPRT, leg_upper.SLDPRT, leg_lower.SLDPRT, hip_actuator.SLDASM,
atlas_rover.SLDASM), version mono (v3.2, v3.2, v3.1, v3.0, v3.2), size,
"derivative" column with small green chips (STEP ✓ glTF ✓), last commit, author.
Row 3 has an amber dot: "leg_lower.SLDPRT — derivative stale (regenerating)".
RIGHT (420px): a dark 3D viewer panel rendering the selected hip_actuator.SLDASM
(grey machined housing, orange stator visible through cutaway), with view cube
and explode slider; under it a "Version history" mini-list (v3.2 current green,
v3.1, v3.0 with mono hashes) and a compare bar "Compare v3.1 ↔ v3.2" with a
ghost button "View Diff".
```

### SCREEN 7 — Electronics page (`/robots/:id/electronics`)

```
Screen: the Electronics (EDA) artifacts page for Atlas Rover; sidebar
"Electronics" active with Altium badge.

Header: "Electronics" title, green pill "Altium 365 connected", blue button
"Open in Altium". Sub-tabs: "Schematics · PCB · BOM · Versions".

Content split: LEFT (fluid): a PCB viewer panel showing a dark-green 4-layer
motor-driver board render (copper pours visible, white silkscreen labels,
JST-GH connectors, XT30 power jack) on a near-black background, with layer
toggle chips (Top, GND1, PWR, Bottom) and 2D/3D toggle; above it a schematic
sheet strip of 3 thumbnails (Power Tree, CAN-FD Bus, MCU + Gate Drivers).
RIGHT (400px): "BOM — hip_driver v1.4.0" panel: compact table (Designator, MPN,
Value, Qty, Stock) — rows like U1 STM32G431CBT6, Q1–Q6 IPT015N10N5, J2
JST-GH-4, C7 100µF/50V; stock column with green dots and one amber "low stock
(120)" warning; footer buttons: ghost "Export CSV", blue "Order Parts ▾". Under
it a small "Power Budget" summary card: "48V rail: 480W provided vs 96.5W
consumed — 20% headroom" with a thin horizontal utilization bar in cyan.
```

### SCREEN 8 — Software page (`/robots/:id/software`)

```
Screen: the Software page for Atlas Rover; sidebar "Software" active.

Header: "Software" title, mono branch pill "main @ a83fd21", green pill
"CI passing", blue button "New Terminal ▾". Sub-tabs: "Packages · Builds ·
Commits · Dependencies".

Content: LEFT (fluid): "Packages" table of ROS 2 packages — name
(atlas_description, atlas_bringup, diff_drive_base, odri_driver, bms_driver,
perception_stack), version mono, license pill (MIT/BSD), build status dot
(green ×5, one amber "odri_driver — 2 warnings"), last commit. Under it a
"Builds" list: rows "#142 main a83fd21 — passed in 4m 12s ✓" green, "#141 —
passed", "#140 — failed (test_nav_recovery)" red with a red ✗, each with
duration bars. RIGHT (400px): "Latest Commit" card (mono hash a83fd21, message
"fix: raise CAN-FD baud to 5Mbit for hip chain", author avatar+name, files
changed +12 −4); under it a "ros2_control" card with a small node graph —
controller_manager node feeding diff_drive_controller and joint_state_broadcaster
nodes, green pass dots; under it a dependencies card: "navigation2 jazzy ✓,
ros_gz harmonic ✓, moveit2 — update available" (amber).
```

### SCREEN 9 — Simulation page (`/robots/:id/simulation`)

```
Screen: the Simulation page for Atlas Rover; sidebar "Simulation" active (Test
mode). Header: "Simulation" title, blue split button "Run Simulation ▾" with
dropdown open showing profile options: "Gazebo · rough_terrain.world · 100
scenarios", "Gazebo · stairs.world · 40 scenarios", "Isaac Sim · warehouse · 20
scenarios".

Content: LEFT (fluid): a live sim viewport panel streaming a Gazebo session —
the quadruped rover mid-walk on rocky dark terrain, physics contact markers in
cyan, a "LIVE" red-dot chip top-left, stream stats chip bottom-right "WebRTC ·
720p · 38 ms"; under it a row of scenario queue cards: "rough_terrain 78/100
done" with a green progress bar, "stairs queued", "flat_ground done ✓".
RIGHT (400px): "Run #248 Results" panel: big "91%" pass ring in green-cyan
gradient; per-scenario rows with pass/fail dots (flat_ground 40/40 ✓,
rough_terrain 71/78 ✓, stairs 12/20 amber); failing scenario row expandable in
red: "stairs_014 — torso pitch exceeded 25° @ t=4.2s" with a ghost button
"Open in Foxglove". Under it an "Environments" status card: Gazebo Running
(green dot), RViz Ready, MoveIt Ready, Isaac Sim Ready, Unity Offline (grey).
```

### SCREEN 10 — Tests & Results page (`/robots/:id/tests`)

```
Screen: the Tests page for Atlas Rover; sidebar "Tests" active under a
VALIDATION group. Header: "Tests" title, filter chips (All · Unit · Integration
· Simulation · HIL · Field · Performance), blue button "Run Suite ▾".

Content: top row of four stat cards: "12/12 suites passing" big green number,
"100% pass rate (7d)", "Mean duration 4m 12s", "Hardware rigs: 2 online". LEFT
(fluid): test suite table — suite name (unit_kinematics, integration_can_bus,
sim_rough_terrain, perf_control_loop, hil_battery_discharge, field_mud_trial),
kind pill (unit cyan, integration blue, simulation purple, performance grey, hil
amber, field grey), last run result (green ✓ pass counts like 12/12, 8/8, 6/6;
the hil_battery_discharge row amber "4/6 — 2 skipped: rig occupied"), duration,
trend sparkline. RIGHT (380px): "Results — integration_can_bus" detail panel:
test rows with green checks and one amber row "test_fd_arbitration_fallback —
flaky (passed on retry 2)"; a small mono log excerpt box with green PASS lines
and one amber WARN line; ghost button "View Full Log", blue button "Re-run".
```

### SCREEN 11 — Releases page (`/robots/:id/releases`)

```
Screen: the Releases page for Atlas Rover; sidebar "Releases" active. Header:
"Releases" title, blue button "New Release".

Content: vertical release timeline, newest first. Each release card: large mono
version "v2.3.1" with green "Latest" pill, date, one-line summary "Hip chain
CAN-FD migration + terrain planner update", a row of artifact chips with domain
icons (URDF bundle ✓, STEP ✓, Gerbers ✓, BOM ✓, Sim world pack ✓, Docs ✓),
manifest diff summary "+3 modules, ~1 module, 14 files changed", and buttons:
ghost "View Manifest", ghost "Download Bundle (.zip)", mono "git tag v2.3.1".
Second card "v2.3.0" similar but with an amber note "superseded — simulation
profile outdated". Third card "v2.2.0" grey. A right-side (340px) panel:
"Release checklist" for a draft v2.3.2 — checklist rows: validation status
"warnings (2)" amber, tests "12/12 ✓" green, licenses "compatible ✓" green,
documentation "missing changelog entry" red, with a disabled grey "Publish
Release" button and hint "Resolve 2 items to publish".
```

### SCREEN 12 — Open Source space (`/open-source`)

```
Screen: the public Open Source robots space (community mode — PURPLE is the
dominant accent here instead of blue). Header: "Open Source Robots" title with
a purple gradient logo variant, search "Search public robots…", filter pills
(Trending · New · Most Cloned · Quadrupeds · Arms · Rovers).

Content: hero strip: three featured robot cards with large renders (an
open-source quadruped "ODRI Solo-12", a 5-axis printed arm "LowCostArm", a
sensor-tower rover "FieldBot") each with purple "Featured" pill, star count,
clone count, license pill (CERN-OHL-P-2.0, MIT). Below, a 4-column grid of
community robot cards: render thumbnail, name, author "@username", stars/forks
mono numbers, license pill, domain completeness dots, purple "Clone" button on
hover. Right rail (300px): "Why open source?" purple-tinted info card ("Every
robot ships with full mechanical, electronics and software manifests — fork a
complete machine, not just code"), "Top contributors" avatar list, "Recently
published" mini-feed with purple timestamps.
```

### SCREEN 13 — Marketplace (`/marketplace`)

```
Screen: the Marketplace page (commerce register: same dark IDE theme, prices in
cyan, keep blue accent). Header: "Marketplace", search "Search modules, robots,
services…", category chips (Actuators · Sensors · Compute · Power · Kits ·
Services), cart icon with badge "2".

Content: LEFT (fluid): product cards in a 3-column grid — "ODRI 60 mm Actuator
kit" €289 with render of the actuator, "verified compatible" green check chip,
vendor "@open-dynamic-robot-initiative", rating 4.9 (128), mono "v1.2.0";
"48V 4Ah BMS pack" €149 (amber "ships in 2 weeks"); "Carbon tube link set
300 mm" €36; "CAN-FD cable harness JST-GH-4" €12; "Atlas Rover — full open kit"
Free (purple "Open Source" pill). RIGHT (320px): cart summary card "Cart (2) —
ODRI actuator ×2, harness ×1, total €590" with blue "Checkout" button; under it
a "Compatibility guarantee" card: "Every purchase is checked against your active
build — 3/3 items compatible with Atlas Rover v2.3.1" with green check list.
```

### SCREEN 14 — Command palette (overlay, any screen)

```
Screen: the Robot Overview dashboard dimmed under a 40% black overlay with the
⌘K command palette open centered at top-third: a 640px floating panel (#111A2A,
stronger border #2A3A5C, 10px radius) with input row "⌕ act" and grouped
results: COMMANDS — "Run Simulation on Gazebo" (play icon), "Create New Module";
FILES — "atlas_rover.SLDASM" (cube icon), "actuator.macro.xacro" (code icon);
MODULES — "ODRI 60 mm Actuator v1.2.0" (chip icon); ROBOTS — "Atlas Arm";
each row with a right-aligned mono kbd hint (↵ open, ⌘R run). Selected first row
highlighted in blue accent-soft rgba(46,124,246,.14) with a blue left bar.
Footer hint row: "↑↓ navigate · ↵ select · esc close".
```

---

## 4. Consistency rules across all images

1. **Same shell everywhere** — identical top bar, sidebar widths, and logo mark in every screen; only the active nav item and content change.
2. **Same robot story** — Atlas Rover, v2.3.1, main, a83fd21, 94% health. Never invent a second demo robot except inside Screen 4 (robots list) and Screen 12 (community).
3. **Color discipline** — if a generator drifts (green buttons, purple status), regenerate; status colors must stay semantic. Blue = actions only.
4. **The robot render inside viewports is always the same quadruped**: grey carbon-fiber legs, orange actuator housings, LiDAR puck on a rear mast.
5. Generate Screen 1 and Screen 2 first; use them as image references ("match the style of this UI") for the rest if your tool supports image prompting.

## 5. Tool-specific tips

- **Midjourney:** append `--ar 16:9 --style raw --v 6`. Keep prompts under ~450 words; if truncated, drop the bottom-strip paragraph.
- **DALL·E 3 / GPT-image:** paste style block + screen block as-is (long prompts OK). Ask for "no photo frame, flat screenshot".
- **SDXL/Flux:** put the negative list in the negative prompt field; CFG 4–6; use a UI-design LoRA if available; upscale 1.5× with a sharpness-focused upscaler rather than re-rolling.
- **Firefly:** choose "Art → UI/UX" style reference if offered; it tends to lighten dark themes — re-state "near-black navy background #070B14" at the END of the prompt too.
