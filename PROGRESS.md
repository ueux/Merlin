# MERLIN — Project Progress

> Living status file. Update at the end of every work session: mark completed items, add a dated log entry, refresh next steps.
> Phase numbering follows `Project-Phases.md` (M0–M9). Started 2026-09-25.

## Status dashboard

| Milestone | Scope | Status | Notes |
|-----------|-------|--------|-------|
| M0 Foundations | Schemas, examples, docs, engine packaging | **DONE** | 3 schemas + 6 examples + full doc set |
| M1 Core | Validation engine, API, web shell | **DONE** | Vertical slice live 2026-09-26 (details below) |
| M2 Software DevOps | ROS 2 packages, builds, repos | pending | UI routes exist as placeholders |
| M3 Modular Builder | Drag-drop canvas + live validation | **NEXT** | Engine ready; needs canvas UI + validate wiring |
| M4 Mechanical | SolidWorks vault, STEP/glTF derivatives | pending | |
| M5 Electrical | Altium 365, DRC, BOM | pending | |
| M6 Materials | Test data plane | pending | |
| M7 Simulation | Gazebo workers, Foxglove, HIL | pending | |
| M8 Publishing | Releases, open-source community, marketplace | pending | |
| M9 Hardening | Auth, scale, GA | pending | |

Deferred from M1: DB-backed registry (directory registry for now, same `resolve()` contract), auth.

## Component inventory

| Component | Path | Status | Verified |
|-----------|------|--------|----------|
| JSON Schemas (robot / module / composition) | `schemas/` | v1.0.0 stable | self-checks + example tests |
| Example manifests + mini-leg composition | `examples/` | stable | validated by engine suite |
| Validation engine `merlin-engine` | `engine/` | v0.1.0 | **68 pytest green** |
| REST API (FastAPI) | `apps/api/` | v0.1.0 | **8 pytest green** |
| Web app (Vite 8 + React 19 + Tailwind v4 + RR7) | `apps/web/` | shell + 2 live screens | tsc/build clean, browser smoke-tested |
| UI/UX prompt pack (14 screens) | `UI-UX-Image-Prompts.md` | done | — |
| Google Stitch reference set (14 screens + 6 renders + code.html) | `stitch_merlin_robot_engineering_platform/` | reviewed | fidelity report delivered 2026-09-26 |

### Web screens

| Screen | Route | Status |
|--------|-------|--------|
| Overview | `/` | **LIVE** (canonical Atlas Rover demo data) |
| Module Registry | `/registry` | **LIVE** — real data from `/api/modules`, manifest drawer |
| Builder, Robots, Software | `/builder` `/robots` `/software` | placeholder (M2/M3) |
| Mechanical, Electronics, Simulation, Tests | … | placeholder (M3–M5) |
| Releases, Marketplace, Open Source | … | placeholder (M5/M8) |

## Run the stack

```bash
# API (terminal 1)
cd apps/api && uvicorn app.main:app --port 8000 --reload

# Web (terminal 2)
cd apps/web && npm run dev          # http://localhost:5173, /api proxied to :8000

# Tests
cd engine && python -m pytest -q    # 68 green
cd apps/api && python -m pytest -q  # 8 green
cd apps/web && npm run build        # type-check + bundle
```

## Known gaps / debts

- Module Builder Stitch screen missing center 3D viewport — re-gen prompt needed before M3 UI build.
- Stitch drift catalogued (ROS distro mix-ups, AXIOM/G-TECH branding, purple bleed in Marketplace) — do not copy blindly from `code.html`.
- `collision` check honestly `skipped` until M4 mesh pipeline; `xacro_compile` static-only until xacro runtime.
- No DB, no auth, no persistence — registry is the `examples/` directory.
- Overview page is static demo data; wire to real robot state when robots plane exists.

## Next steps (priority order)

1. **M3 Builder canvas**: module palette (from `/api/modules`) → drag onto canvas → instances/mates state → `POST /compositions/validate` on every change → render 7-check results inline (incl. INCOMPATIBLE error state per Stitch screen 3).
2. Robots gallery page (`/robots`) backed by a robot-manifest endpoint.
3. Composition save/load (JSON download/upload) so builder output persists as files.
4. Then M2 software plane pages.

## Log

- **2026-09-25** — Project founded: research (5 domains), Project-Report, PRD, Mindmap, Frontend-Design, Backend-System-Design, README, Project-Phases. 3 schemas + 6 examples drafted and validated.
- **2026-09-26 (am)** — `merlin-engine` v0.1.0: 7 checks + license engine, 67 tests green, CLI. Schema relaxations for partial assemblies (instances ≥1, mates ≥0).
- **2026-09-26 (pm)** — M1 vertical slice: FastAPI service (8 tests), web app shell + Overview + live Registry, full-stack browser smoke test green. Progress file created.
