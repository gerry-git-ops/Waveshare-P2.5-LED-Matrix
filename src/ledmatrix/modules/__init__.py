"""Available modules and a helper to build them from the config."""

from ledmatrix.config import ModuleConfig
from ledmatrix.modules.base import Module
from ledmatrix.modules.clock import Clock

# name in config.yaml -> module class
REGISTRY: dict[str, type[Module]] = {
    "clock": Clock,
}


def create_module(cfg: ModuleConfig, width: int, height: int) -> Module:
    """Build one module from its config entry."""
    try:
        cls = REGISTRY[cfg.type]
    except KeyError:
        known = ", ".join(sorted(REGISTRY))
        raise ValueError(f"Unknown module type '{cfg.type}'. Known: {known}") from None
    module = cls(width, height, **(cfg.model_extra or {}))
    module.duration = cfg.duration
    return module