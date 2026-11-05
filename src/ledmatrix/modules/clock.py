"""Digital clock."""

import time

from PIL import Image, ImageDraw, ImageFont

from ledmatrix.modules.base import Module


class Clock(Module):
    """Shows the current time, centered and scaled to the display."""

    def __init__(self, width: int, height: int,
                 color: tuple[int, int, int] = (255, 255, 255),
                 fmt: str = "%H:%M:%S") -> None:
        super().__init__(width, height)
        self.color = tuple(color)
        self.fmt = fmt
        self.font = self._fit_font(time.strftime(fmt))

    def _fit_font(self, sample: str) -> ImageFont.FreeTypeFont:
        """Pick the largest font size that still fits the display."""
        size = self.height
        while size > 6:
            font = ImageFont.load_default(size=size)
            left, top, right, bottom = font.getbbox(sample)
            if right - left <= self.width - 4 and bottom - top <= self.height - 4:
                return font
            size -= 1
        return ImageFont.load_default(size=6)

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        text = time.strftime(self.fmt)
        draw.text((self.width / 2, self.height / 2), text,
                  font=self.font, fill=self.color, anchor="mm")
        return img