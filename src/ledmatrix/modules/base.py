"""Base class for all display modules."""

from abc import ABC, abstractmethod

from PIL import Image


class Module(ABC):
    """A module draws one image per frame."""

    duration: float = 10.0  # seconds on screen before the next module
    name: str = ""          # type in config.yaml, e.g. "clock" (set by create_module)
    config_index: int = -1  # position in the module list of config.yaml

    # translations: {"en": {"key": "text", ...}, "de": {...}, ...}
    texts: dict[str, dict[str, str]] = {}

    def __init__(self, width: int, height: int, language: str = "en",
                 overrides: dict[str, str] | None = None) -> None:
        self.width = width
        self.height = height
        self.language = language
        self.overrides = overrides or {}

    def text(self, key: str) -> str:
        """Text in the configured language, English as fallback."""
        if key in self.overrides:
            return self.overrides[key]
        for lang in (self.language, "en"):
            if key in self.texts.get(lang, {}):
                return self.texts[lang][key]
        return key

    def start(self) -> None:
        """Called each time the module becomes active (optional)."""

    @abstractmethod
    def render(self, t: float) -> Image.Image:
        """Return the frame for t seconds after start()."""