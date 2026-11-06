"""Falling snow widget."""

import math
import random

from PIL import Image, ImageDraw

from ledmatrix.widgets.base import Widget


class Snow(Widget):
    """Snowflakes that fall down and sway gently from side to side."""

    def __init__(self, width: int, height: int, count: int = 40,
                 color: tuple[int, int, int] = (110, 110, 130)) -> None:
        super().__init__(width, height)
        self.count = count
        self.color = tuple(color)
        self.flakes: list[tuple[float, float, float, float]] = []

    def start(self) -> None:
        # new snowflakes every time the module becomes active
        rnd = random.Random()
        self.flakes = [
            (rnd.uniform(0, self.width), rnd.uniform(0, self.height),
             rnd.uniform(5, 12), rnd.uniform(0, math.tau))
            for _ in range(self.count)
        ]

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        draw = ImageDraw.Draw(img)
        for x0, y0, speed, phase in self.flakes:
            fy = (y0 + speed * t) % self.height
            fx = (x0 + 2 * math.sin(t + phase)) % self.width
            draw.point((x + fx, y + fy), fill=self.color)