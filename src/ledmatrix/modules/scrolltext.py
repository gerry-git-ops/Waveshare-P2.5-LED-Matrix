"""Scrolling text."""

import colorsys

from PIL import Image, ImageDraw

from ledmatrix.fonts import fit_font
from ledmatrix.modules.base import Module


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
        self.speed = speed  # pixels per second
        text = self.text("text")
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
        self.duration = loops * self.distance / speed

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        # start just outside the right edge, move left, start over when gone
        x = self.width - int(t * self.speed) % self.distance
        img.paste(self.strip, (x, 0))
        return img