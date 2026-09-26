---
name: Robotics Engineering Workstation
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e17'
  surface-container-low: '#171c25'
  surface-container: '#1b2029'
  surface-container-high: '#262a34'
  surface-container-highest: '#31353f'
  on-surface: '#dfe2f0'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#dfe2f0'
  inverse-on-surface: '#2c303b'
  outline: '#8c90a0'
  outline-variant: '#424754'
  surface-tint: '#aec6ff'
  primary: '#aec6ff'
  on-primary: '#002e6b'
  primary-container: '#4f8eff'
  on-primary-container: '#00275e'
  inverse-primary: '#005ac4'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#4cd7f6'
  on-tertiary: '#003640'
  tertiary-container: '#009eb9'
  on-tertiary-container: '#002f38'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#aec6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004396'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#acedff'
  tertiary-fixed-dim: '#4cd7f6'
  on-tertiary-fixed: '#001f26'
  on-tertiary-fixed-variant: '#004e5c'
  background: '#0f131d'
  on-background: '#dfe2f0'
  surface-variant: '#31353f'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: '600'
    lineHeight: 2rem
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: '600'
    lineHeight: 1.5rem
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: '600'
    lineHeight: 1.25rem
    letterSpacing: -0.01em
  body-md:
    fontFamily: Inter
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.25rem
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: '400'
    lineHeight: 1rem
    letterSpacing: 0em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 0.8125rem
    fontWeight: '400'
    lineHeight: 1.25rem
    letterSpacing: -0.01em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 0.6875rem
    fontWeight: '500'
    lineHeight: 0.875rem
    letterSpacing: 0.02em
  badge-label:
    fontFamily: JetBrains Mono
    fontSize: 0.625rem
    fontWeight: '600'
    lineHeight: 0.75rem
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 0.5rem
  margin: 0.75rem
  space-xs: 0.25rem
  space-sm: 0.375rem
  space-md: 0.5rem
  space-lg: 0.75rem
  space-xl: 1rem
---

## Brand & Style

This design system delivers a high-density, mission-critical workspace tailored for robotics engineers, firmware architects, and hardware-in-the-loop operators. The aesthetic merges the disciplined precision of modern developer tools with the structured spatial authority of industrial CAD workstations and real-time telemetry consoles.

The interface prioritizes maximum signal-to-noise ratio, ultra-crisp boundary definition, and immediate scanability. Depth is achieved entirely through structural surface stratification and hairline strokes rather than diffused drop shadows or blurred physical simulations. The emotional tone is authoritative, instrument-grade, and computational: every pixel serves telemetry tracking, kinematic validation, hardware configuration, or code synthesis.

## Colors

The palette is engineered for prolonged sessions under demanding environmental lighting conditions, anchored in an ink-deep, near-black navy foundation.

### Surface System
- **Canvas Base**: `#070B14` — Deep workspace background behind docked panels and viewport canvases.
- **Surface Level 1 (Panels)**: `#0D1420` — Primary module containers, toolbars, sidebar navigations, and telemetry docks.
- **Surface Level 2 (Nested Panels / Wells)**: `#111A2A` — Embedded inspectors, code editors, data grids, log outputs, and input backgrounds.
- **Surface Level 3 (Active / Hover / Float)**: `#192438` — Hovered rows, floating tooltips, flyout popovers, and activated list nodes.

### Stroke & Structural Grids
- **Panel Border**: `#1C2740` — Strict 1px boundary separating all panels, docks, and header divisions.
- **Subtle Divider**: `#162035` — Hairline delimiters within lists, table cells, and button groups.
- **Interactive Border**: `#2A3A5E` — Default perimeter for inputs and inactive controls; transitions to `#2E7CF6` on focus.

### Accent & Signal Palette
- **Primary Accent**: `#2E7CF6` — Interactive focus, active navigation tabs, execution primaries, and selected joint states.
- **Community & OS**: `#8B5CF6` — Open-source module badges, package registries, and peer-to-peer workspace hooks.
- **Informational**: `#06B6D4` — Sensor telemetry metrics, bus data, and non-blocking notifications.
- **System Pass / Nominal**: `#22C55E` — Motor nominal status, kinematic pass, and valid CI/CD compilation.
- **System Warning / Degraded**: `#F59E0B` — Thermal threshold cautions, payload limit warnings, and uncommitted manifests.
- **System Error / Critical Fault**: `#EF4444` — E-stop trips, actuator stall errors, buffer overruns, and failed assertions.

### Monochromatic Hierarchy
- **Text Primary**: `#F1F5F9` — Readouts, titles, critical data figures, and primary interface labels.
- **Text Secondary**: `#8FA1BC` — Field headers, property attributes, structural navigation labels, and unit metrics.
- **Text Muted**: `#5B6B87` — Disabled actions, timestamps, subtle annotations, and structural brackets.

## Typography

The typographic hierarchy enforces clear visual separation between semantic interface structure and raw execution data.

- **Primary UI (Inter)**: Handles layout headers, property keys, tool navigation, and contextual descriptions. Inter is set with compact vertical proportions and subtle negative tracking on medium-to-large sizes to prevent visual sprawl across high-density tool racks.
- **Precision Data & Code (JetBrains Mono)**: Reserved for commit hashes, kinematic matrices, motor angles, sensor telemetry streams, terminal outputs, and system badges. Figures are rendered strictly with tabular spacing (`tnum`) and slashed zeros to ensure instantaneous column alignment during continuous value updates.
- **Scale Compactness**: Font sizes do not exceed `1.5rem` (`24px`). In a multi-pane robotics workstation, oversized titles waste critical view space needed for 3D viewports, diagnostic plots, and logic trees.

## Layout & Spacing

The workstation operates on an ultra-compact 4px modular spacing grid designed for docking panels, splitters, and multi-viewport orchestration.

### Layout Model
- **Docking Workstation Grid**: The canvas uses zero-margin fluid layouts divided by 1px `#1C2740` splitters. Content does not float loosely; it is housed in structured container frames that maximize viewable operational surfaces.
- **Split Pane Hierarchy**: Root application containers dock seamlessly across top-level control bars (height: 40px), primary left/right sidebars (standard: 280px to 360px), lower log terminals (collapsible, min-height: 160px), and central 3D/telemetry viewports.
- **Information Density**: Internal panel padding defaults to `space-md` (`8px`) or `space-sm` (`6px`). Data rows, inspector trees, and node graphs strictly use 24px–28px cell heights to allow dozens of parameters to remain visible above the fold.
- **Responsive Adaptations**:
  - **Desktop / Multi-Monitor (≥1440px)**: Default 3-pane or 4-pane simultaneous docking with active split resizing.
  - **Laptop (1024px – 1439px)**: Sidebars collapse to icon-rail panels (width: 48px), log terminal switches to overlay mode.
  - **Field Tablet (<1024px)**: Single-active-pane view with bottom sheet switching for telemetry diagnostics and manual joint override controls.

## Elevation & Depth

This design system deliberately eliminates diffused ambient drop shadows (`box-shadow: none`) in favor of an architectural, edge-defined planar hierarchy. Elevation is represented through calibrated surface illumination and high-contrast perimeter strokes.

- **Level 0 (Canvas Floor - `#070B14`)**: Viewport canvases, raw 3D scene renders, and empty docking bays.
- **Level 1 (Docked Containers - `#0D1420`)**: Standard workstation panels. Defined with a uniform `1px solid #1C2740` boundary.
- **Level 2 (Recessed Regions - `#111A2A`)**: Input fields, telemetry log blocks, code viewports, and table headers. Sinks into the panel surface with an internal `1px solid #162035` perimeter border.
- **Level 3 (Floating Overlays - `#192438`)**: Command palettes, context menus, and tooltips. Elevated above the viewport with a crisp `1px solid #2E7CF6` (primary highlight) or `1px solid #2A3A5E` border, without outer blur diffusion.

## Shapes

The geometric framework balances technical rigor with modern ergonomics by establishing a universal `10px` corner radius (`0.625rem`) for macro-level structural containers, while micro-elements maintain tighter corner profiles to optimize visual packing.

- **Panels & Modules**: Fixed at `10px` (`rounded-xl` in the context of this system) to establish distinct modular boundaries against the dark navy base.
- **Inputs, Buttons, & Interactive Wells**: Standardized at `6px` (`rounded-md`), preserving geometric order within high-density parameter stacks without appearing overly rounded or toy-like.
- **Status Pills & Micro Badges**: Scaled down to `4px` or fully encapsulated pill configurations (`9999px`) strictly for atomic status indicators and channel counters.

## Components

### Buttons & Trigger Controls
- **Primary Action**: Background `#2E7CF6`, label `#F1F5F9` (Inter 600, 12px), border `1px solid transparent`. Hover shifts background to `#3B82F6`. Active state shifts to `#1D4ED8`. Focus ring: `1px solid #F1F5F9` offset by 2px `#070B14`.
- **Secondary / Panel Action**: Background `#111A2A`, label `#8FA1BC`, border `1px solid #1C2740`. On hover: border `#2A3A5E`, label `#F1F5F9`, background `#192438`.
- **Critical / E-Stop**: Background `rgba(239, 68, 68, 0.12)`, label `#EF4444`, border `1px solid rgba(239, 68, 68, 0.4)`. Active state fills solid `#EF4444` with white text.
- **Height Scale**: Compact buttons are strictly 24px or 28px tall; primary workstation triggers do not exceed 32px.

### Badges, Pills & Indicators
- **Technical Badges**: Composed with JetBrains Mono, 10px uppercase, `tracking-wide`. Padding is 2px top/bottom, 6px left/right.
- **Status Styles**:
  - *Pass / Healthy*: Background `rgba(34, 197, 94, 0.1)`, text `#22C55E`, border `1px solid rgba(34, 197, 94, 0.25)`.
  - *Warning / Degraded*: Background `rgba(245, 158, 11, 0.1)`, text `#F59E0B`, border `1px solid rgba(245, 158, 11, 0.25)`.
  - *Critical / Error*: Background `rgba(239, 68, 68, 0.1)`, text `#EF4444`, border `1px solid rgba(239, 68, 68, 0.25)`.
  - *Telemetry / Cyan*: Background `rgba(6, 182, 212, 0.1)`, text `#06B6D4`, border `1px solid rgba(6, 182, 212, 0.25)`.
  - *Community / Package*: Background `rgba(139, 92, 246, 0.1)`, text `#8B5CF6`, border `1px solid rgba(139, 92, 246, 0.25)`.
- **Pill Dot Indicators**: 6px circular dot centered vertically with corresponding status color, pulsating only on active hardware-in-the-loop streaming.

### Data Tables & Tree Lists
- **Structure**: Surface `#0D1420`, cell dividers `1px solid #162035`.
- **Header Row**: Height 24px, background `#090E17`, text `#5B6B87` (Inter 600, 11px uppercase, tracking-wider).
- **Body Rows**: Height 26px to 28px, text `#8FA1BC`, numerical outputs `#F1F5F9` in JetBrains Mono. Selected row: background `#111A2A` with a 2px left border accent of `#2E7CF6`.

### Inputs, Sliders & Numerical Fields
- **Text & Numeric Inputs**: Background `#111A2A`, border `1px solid #1C2740`, text `#F1F5F9`, placeholder `#5B6B87`. Height 26px, padding 0 8px, border-radius 6px. Focused state replaces border with `#2E7CF6` and zero drop shadow.
- **Dual-Unit Displays**: Integrated right-aligned unit indicator (`rad`, `mm`, `rpm`, `V`) rendered in JetBrains Mono `#5B6B87`.
- **Scrubbable Numeric Drag Fields**: Numeric input cursor switches to `ew-resize`, active drag adds a thin 1px `#2E7CF6` underline.

### Cards & Modular Dock Panels
- **Container Architecture**: Outer background `#0D1420`, border `1px solid #1C2740`, corner radius `10px`.
- **Panel Header**: Height 32px, padding `0 10px`, background `#0A0F18`, bottom border `1px solid #1C2740`. Displays pane title in Inter 600 (11px, `#8FA1BC`), trailing actions (detach, minimize, close), and telemetry status indicators.
- **Embedded Inspector Wells**: Nested sub-panels use background `#111A2A`, corner radius `6px`, and border `1px solid #162035`.

### Checkboxes, Toggles & Radios
- **Checkboxes**: 14px × 14px squares, background `#111A2A`, border `1px solid #2A3A5E`, border-radius 3px. Checked state: background `#2E7CF6`, border `#2E7CF6`, checkmark icon `#FFFFFF`.
- **Hardware Toggle Switches**: Width 28px, height 16px, track background `#162035`, active track `#2E7CF6`. Thumb: 12px white circle with zero blur shadow, transitioning horizontally with a 150ms linear curve.