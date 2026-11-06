"""Water widget."""

import math

from PIL import Image, ImageDraw

from ledmatrix.widgets.base import Widget


class Water(Widget):
    """Water surface with short moving wave highlights."""

    def __init__(self, width: int, height: int,
                 back: tuple[int, int, int] = (4, 28, 70),
                 front: tuple[int, int, int] = (8, 38, 90)) -> None:
        super().__init__(width, height)
        self.gradient = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(self.gradient)
        for y in range(height):
            a = y / max(1, height - 1)
            color = tuple(int(c0 + (c1 - c0) * a) for c0, c1 in zip(back, front))
            draw.line((0, y, width, y), fill=color)

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        area = self.gradient.copy()
        draw = ImageDraw.Draw(area)
        for row in range(2, self.height, 3):
            k = row / max(1, self.height)              # 0 = far away, 1 = in front
            for i in range(0, self.width, 9):
                # waves in front are longer and move faster, that gives depth
                wx = (i + t * (6 + 10 * k) + row * 5) % self.width
                glow = int(60 + 60 * (0.5 + 0.5 * math.sin(t * 2 + i + row)))
                draw.line((wx, row, wx + 1 + int(3 * k), row), fill=(20, 60 + glow // 2, 100 + glow))
        img.paste(area, (x, y))