"""Sky widget."""

import random

from PIL import Image, ImageDraw, ImageFilter

from ledmatrix.widgets.base import Widget


class Sky(Widget):
    """Sky that gets lighter towards the bottom, with drifting clouds."""

    def __init__(self, width: int, height: int, clouds: int = 3,
                 top: tuple[int, int, int] = (4, 8, 30),
                 bottom: tuple[int, int, int] = (22, 48, 110)) -> None:
        super().__init__(width, height)
        self.cloud_count = clouds
        self.clouds: list[tuple[float, float, float, int]] = []
        self.cloud = self._cloud()

        # the color gradient is drawn once, every frame only copies it
        self.gradient = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(self.gradient)
        for y in range(height):
            a = y / max(1, height - 1)
            color = tuple(int(c0 + (c1 - c0) * a) for c0, c1 in zip(top, bottom))
            draw.line((0, y, width, y), fill=color)

    def _cloud(self) -> Image.Image:
        """Soft cloud shape made of a few circles, used as a mask."""
        mask = Image.new("L", (40, 14))
        draw = ImageDraw.Draw(mask)
        for cx, cy, r in [(10, 9, 5), (18, 6, 6), (27, 8, 5), (33, 10, 4), (14, 11, 4)]:
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=150)
        return mask.filter(ImageFilter.GaussianBlur(1.2))

    def start(self) -> None:
        # new clouds every time: x, y, speed (px/s), brightness
        rnd = random.Random()
        self.clouds = [(rnd.uniform(0, self.width), rnd.uniform(0, self.height * 0.4),
                        rnd.uniform(1.5, 4.0), rnd.randint(45, 70))
                       for _ in range(self.cloud_count)]

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        area = self.gradient.copy()
        for cx, cy, speed, b in self.clouds:
            # drift to the left, come back on the right
            px = (cx - speed * t) % (self.width + 40) - 40
            area.paste((b, b + 10, b + 40), (int(px), int(cy)), self.cloud)
        img.paste(area, (x, y))