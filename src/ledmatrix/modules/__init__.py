"""Available modules and a helper to build them from the config."""

from ledmatrix.config import ModuleConfig
from ledmatrix.modules.base import Module
from ledmatrix.modules.clock import Clock
from ledmatrix.modules.christmas import Christmas
from ledmatrix.modules.scrolltext import ScrollText
from ledmatrix.modules.gif import GifPlayer
from ledmatrix.modules.countdown import CountdownModule
from ledmatrix.modules.voyage import Voyage

# name in config.yaml -> module class
REGISTRY: dict[str, type[Module]] = {
    "clock": Clock,
    "christmas": Christmas,
    "scrolltext": ScrollText,
    "gif": GifPlayer,
    "countdown": CountdownModule,
    "voyage": Voyage,
}

def create_module(cfg: ModuleConfig, width: int, height: int,
                  language: str = "en") -> Module:
    """Build one module from its config entry."""
    try:
        cls = REGISTRY[cfg.type]
    except KeyError:
        known = ", ".join(sorted(REGISTRY))
        raise ValueError(f"Unknown module type '{cfg.type}'. Known: {known}") from None

    options = dict(cfg.model_extra or {})
    # options that match a text key of the module replace that text
    text_keys = set(cls.texts.get("en", {}))
    overrides = {key: options.pop(key) for key in list(options) if key in text_keys}

    module = cls(width, height, language=language, overrides=overrides, **options)
    if cfg.duration is not None:
        module.duration = cfg.duration
    return module