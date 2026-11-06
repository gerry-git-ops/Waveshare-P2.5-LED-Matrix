"""Scrolling text widget."""

import colorsys

from PIL import Image, ImageDraw

from ledmatrix.fonts import fit_font
from ledmatrix.widgets.base import Widget


class ScrollingText(Widget):
    """Text that moves from right to left through its area."""

    def __init__(self, width: int, height: int, text: str,
                 color: tuple[int, int, int] = (255, 255, 255),
                 rainbow: bool = False,
                 speed: float = 40,
                 size: float = 0.6) -> None:
        super().__init__(width, height)
        self.speed = speed  # pixels per second
        font = fit_font(text, 10_000, int(height * size))

        # draw the text once into a strip, scrolling just moves this strip
        left, top, right, bottom = font.getbbox(text)
        self.strip = Image.new("RGB", (right - left, height))
        draw = ImageDraw.Draw(self.strip)
        y = height / 2
        if rainbow:
            x = -left
            for i, char in enumerate(text):
                r, g, b = colorsys.hsv_to_rgb((i * 0.07) % 1.0, 1.0, 1.0)
                draw.text((x, y), char, font=font, fill=(int(r * 255), int(g * 255), int(b * 255)),
                          anchor="lm")
                x += font.getlength(char)
        else:
            draw.text((-left, y), text, font=font, fill=tuple(color), anchor="lm")

        # one pass = from the right edge until the text has left on the left side
        self.distance = width + self.strip.width

    def pass_time(self) -> float:
        """Seconds for one complete pass."""
        return self.distance / self.speed

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        offset = self.width - int(t * self.speed) % self.distance
        # cut out the visible part, so nothing is drawn outside the widget area
        visible = self.strip.crop((-offset, 0, -offset + self.width, self.height))
        img.paste(visible, (x, y))