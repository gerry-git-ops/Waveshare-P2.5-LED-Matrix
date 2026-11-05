"""Base class for all widgets."""

from abc import ABC, abstractmethod

from PIL import Image


class Widget(ABC):
    """Draws one thing into a rectangular area of the frame."""

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

    def start(self) -> None:
        """Called when the module that owns the widget becomes active (optional)."""

    @abstractmethod
    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        """Draw onto img, with the top left corner of the widget at (x, y)."""