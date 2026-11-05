"""Digital clock."""

import time

from PIL import Image, ImageDraw

from ledmatrix.fonts import fit_font
from ledmatrix.modules.base import Module


class Clock(Module):
    """Shows the current time, centered and scaled to the display."""

    def __init__(self, width: int, height: int,
                 color: tuple[int, int, int] = (255, 255, 255),
                 fmt: str = "%H:%M:%S",
                 **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        self.color = tuple(color)
        self.fmt = fmt
        self.font = fit_font(time.strftime(fmt), width - 4, height - 4)

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        text = time.strftime(self.fmt)
        draw.text((self.width / 2, self.height / 2), text,
                  font=self.font, fill=self.color, anchor="mm")
        return img