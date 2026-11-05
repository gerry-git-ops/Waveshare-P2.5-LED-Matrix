"""Base class for all display modules."""

from abc import ABC, abstractmethod

from PIL import Image


class Module(ABC):
    """A module draws one image per frame."""

    duration: float = 10.0  # seconds on screen before the next module

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def start(self) -> None:
        """Called each time the module becomes active (optional)."""

    @abstractmethod
    def render(self, t: float) -> Image.Image:
        """Return the frame for t seconds after start()."""