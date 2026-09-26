"""Resolution layer: turns an authored composition doc into a queryable context.

Structural problems (unresolvable modules, broken parent links, dangling refs)
are collected in ctx.errors; checks then operate on whatever did resolve.
"""

from __future__ import annotations

from .errors import RegistryError
from .registry import ModuleRegistry


class CompositionContext:
    def __init__(self, doc: dict, registry: ModuleRegistry):
        self.doc = doc
        self.registry = registry
        self.errors: list[str] = []
        self.instances: dict[str, dict] = {}
        self.modules: dict[str, dict] = {}  # instance id -> module manifest
        self.children: dict[str, list[str]] = {}
        self.roots: list[str] = []
        self._resolve_instances()
        self._resolve_parents()

    # -- resolution ---------------------------------------------------------

    def _resolve_instances(self) -> None:
        for inst in self.doc.get("instances", []):
            iid = inst["id"]
            if iid in self.instances:
                self.errors.append(f"duplicate instance id: {iid!r}")
                continue
            self.instances[iid] = inst
        for inst in self.instances.values():
            key = (inst["module_id"], inst["module_version"])
            try:
                self.modules[inst["id"]] = self.registry.resolve(*key)
            except RegistryError as e:
                self.errors.append(f"instance {inst['id']!r}: {e}")

    def _resolve_parents(self) -> None:
        for inst in self.instances.values():
            self.children[inst["id"]] = []
        for inst in self.instances.values():
            parent = inst.get("parent")
            if parent is None:
                self.roots.append(inst["id"])
                continue
            pid, frame = parent["instance"], parent["frame"]
            if pid == inst["id"]:
                self.errors.append(f"instance {inst['id']!r}: cannot be its own parent")
                continue
            if pid not in self.instances:
                self.errors.append(f"instance {inst['id']!r}: parent instance {pid!r} does not exist")
                continue
            pmod = self.modules.get(pid)
            if pmod is not None and not self._module_has_frame(pmod, frame):
                self.errors.append(
                    f"instance {inst['id']!r}: parent frame {frame!r} not declared on module "
                    f"{pmod['module']['id']} (frames: {', '.join(f['id'] for f in pmod['mechanical']['frames'])})"
                )
                continue
            self.children[pid].append(inst["id"])
        self._check_cycles_and_connectivity()

    def _check_cycles_and_connectivity(self) -> None:
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {iid: WHITE for iid in self.instances}
        reachable: set[str] = set()

        def visit(iid: str, stack: list[str]) -> None:
            color[iid] = GRAY
            reachable.add(iid)
            for child in self.children.get(iid, []):
                if color[child] == GRAY:
                    cycle = " -> ".join(stack + [iid, child])
                    self.errors.append(f"parent graph contains a cycle: {cycle}")
                    continue
                if color[child] == WHITE:
                    visit(child, stack + [iid])
            color[iid] = BLACK

        for root in self.roots:
            if color[root] == WHITE:
                visit(root, [])
        orphans = sorted(set(self.instances) - reachable)
        if orphans:
            self.errors.append(
                f"instances not reachable from any root (disconnected assembly): {', '.join(orphans)}"
            )
        if not self.roots and self.instances:
            self.errors.append("no root instance (every instance has a parent)")

    # -- queries ------------------------------------------------------------

    @staticmethod
    def _module_has_frame(module: dict, frame: str) -> bool:
        return any(f["id"] == frame for f in module["mechanical"]["frames"])

    def module_of(self, instance_id: str) -> dict | None:
        return self.modules.get(instance_id)

    def mech_interface(self, instance_id: str, interface_id: str) -> dict | None:
        module = self.modules.get(instance_id)
        if module is None:
            return None
        for iface in module["mechanical"]["interfaces"]:
            if iface["id"] == interface_id:
                return iface
        return None

    def bus(self, instance_id: str, port_id: str) -> dict | None:
        module = self.modules.get(instance_id)
        if module is None:
            return None
        for b in module.get("electrical", {}).get("buses", []):
            if b["id"] == port_id:
                return b
        return None

    def power_port(self, instance_id: str, port_id: str) -> dict | None:
        module = self.modules.get(instance_id)
        if module is None:
            return None
        for p in module.get("electrical", {}).get("power", []):
            if p["id"] == port_id:
                return p
        return None

    def sw_interface(self, instance_id: str, interface_id: str) -> dict | None:
        module = self.modules.get(instance_id)
        if module is None:
            return None
        for s in module.get("software", {}).get("interfaces", []):
            if s["id"] == interface_id:
                return s
        return None

    def downstream_mass(self, instance_id: str) -> float:
        """Mass of this instance plus everything attached beneath it (kg). Cycle-safe."""
        seen: set[str] = set()

        def walk(iid: str) -> float:
            if iid in seen:
                return 0.0
            seen.add(iid)
            module = self.modules.get(iid)
            own = module["mechanical"]["mass_kg"] if module else 0.0
            return own + sum(walk(c) for c in self.children.get(iid, []))

        return walk(instance_id)

    def ancestors(self, instance_id: str) -> set[str]:
        result: set[str] = set()
        current = self.instances[instance_id].get("parent")
        while current is not None:
            pid = current["instance"]
            if pid in result or pid not in self.instances:
                break
            result.add(pid)
            current = self.instances[pid].get("parent")
        return result
