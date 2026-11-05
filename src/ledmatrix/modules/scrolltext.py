"""Scrolling text over the whole display."""

from PIL import Image

from ledmatrix.modules.base import Module
from ledmatrix.widgets.scrolling_text import ScrollingText


class ScrollText(Module):
    """Text that moves from right to left across the display."""

    texts = {
        "en": {"text": "Hello from the LED matrix!"},
        "de": {"text": "Hallo von der LED-Matrix!"},
        "fr": {"text": "Bonjour de la matrice LED !"},
        "es": {"text": "¡Hola desde la matriz LED!"},
    }

    def __init__(self, width: int, height: int,
                 color: tuple[int, int, int] = (255, 255, 255),
                 rainbow: bool = False,
                 speed: float = 40,
                 size: float = 0.6,
                 loops: int = 1,
                 **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        self.scroller = ScrollingText(width, height, self.text("text"),
                                      color=color, rainbow=rainbow, speed=speed, size=size)
        self.duration = loops * self.scroller.pass_time()

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        self.scroller.draw(img, 0, 0, t)
        return img