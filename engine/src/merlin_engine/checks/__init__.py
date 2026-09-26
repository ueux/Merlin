"""The 7 composition checks. Names match the composition schema's checkResult enum exactly."""

from .mate_matching import check_mate_matching
from .load_rating import check_load_rating
from .collision import check_collision
from .power_budget import check_power_budget
from .bus_config import check_bus_config
from .software_interfaces import check_software_interfaces
from .xacro_compile import check_xacro_compile

# Ordered to match the schema enum; the engine always returns all 7.
CHECKS = [
    ("check-mates", "mate_matching", check_mate_matching),
    ("check-loads", "load_rating", check_load_rating),
    ("check-collision", "collision", check_collision),
    ("check-power", "power_budget", check_power_budget),
    ("check-bus", "bus_config", check_bus_config),
    ("check-sw", "software_interfaces", check_software_interfaces),
    ("check-xacro", "xacro_compile", check_xacro_compile),
]

__all__ = ["CHECKS"]
