"""Particle widget: burst an image into single pixels and gather them into another one."""

import math
import random
from typing import Callable

from PIL import Image, ImageDraw

from ledmatrix.widgets.base import Widget

Point = tuple[float, float]
Color = tuple[int, int, int]


def smooth(a: float) -> float:
    """0..1 with a soft start and a soft end."""
    a = max(0.0, min(1.0, a))
    return a * a * (3 - 2 * a)


class Particles(Widget):
    """Many single pixels that fly apart and come together again."""

    def __init__(self, width: int, height: int, gravity: float = 10.0, drag: float = 1.1) -> None:
        super().__init__(width, height)
        self.gravity = gravity      # pixels per second², pulls downwards
        self.drag = drag            # how fast the pixels slow down
        self.parts: list[dict] = []
        self.gather_t: float | None = None
        self.attractor: Callable[[float], Point] | None = None
        self.pull_time = 1.2
        self.travel = 0.9

    @staticmethod
    def pixels(img: Image.Image, threshold: int = 120) -> list[tuple[int, int, Color]]:
        """All pixels of img that are bright enough, as (x, y, color)."""
        px = img.convert("RGB").load()
        return [(x, y, px[x, y]) for y in range(img.height) for x in range(img.width)
                if sum(px[x, y]) > threshold]

    def burst(self, img: Image.Image, origin: Point, t: float,
              speed: tuple[float, float] = (30, 110)) -> None:
        """The lit pixels of img fly away from origin, starting at time t."""
        rnd = random.Random()
        ox, oy = origin
        self.parts = []
        for x, y, color in self.pixels(img):
            angle = math.atan2(y - oy, x - ox) + rnd.uniform(-0.6, 0.6)
            v = rnd.uniform(*speed)
            self.parts.append({"x": x, "y": y, "c": color, "t0": t,
                               "vx": math.cos(angle) * v, "vy": math.sin(angle) * v - 20})
        self.gather_t = None

    def gather(self, img: Image.Image, t: float,
               attractor: Callable[[float], Point] | None = None,
               release: Callable[[float], float] | None = None,
               pull_time: float = 1.2, travel: float = 0.9) -> None:
        """From time t on, the pixels fly into the lit pixels of img.

        attractor(t) -> (x, y): a moving point that pulls the pixels along first (optional).
        release(x) -> time: when the pixel for column x is let go to its place (optional).
        """
        rnd = random.Random()
        targets = self.pixels(img)
        while self.parts and len(self.parts) < len(targets):
            self.parts.append(dict(rnd.choice(self.parts)))   # not enough pixels: copy some
        # right side first, so the picture fills up behind something moving to the left
        ordered = sorted(self.parts, key=lambda p: -p["x"])
        for p, (tx, ty, tc) in zip(ordered, sorted(targets, key=lambda q: -q[0])):
            p["target"] = (tx, ty, tc)
            p["release"] = (release(tx) if release else t) + rnd.uniform(0, 0.25)
        self.gather_t, self.attractor = t, attractor
        self.pull_time, self.travel = pull_time, travel

    def _flying(self, p: dict, t: float) -> Point:
        """Position while flying freely after the burst: slows down, falls slowly."""
        dt = max(0.0, t - p["t0"])
        k = (1 - math.exp(-dt * self.drag)) / self.drag
        return p["x"] + p["vx"] * k, p["y"] + p["vy"] * k + self.gravity * dt * dt

    def _pulled(self, p: dict, t: float) -> Point:
        """Position while being pulled along by the attractor."""
        x, y = self._flying(p, t)
        if self.attractor is None or self.gather_t is None:
            return x, y
        pull = 0.85 * smooth((t - self.gather_t) / self.pull_time)
        ax, ay = self.attractor(t)
        ax += 3 * math.sin(t * 9 + p["x"])        # a little swirl
        ay += 3 * math.cos(t * 7 + p["y"])
        return x + (ax - x) * pull, y + (ay - y) * pull

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        draw = ImageDraw.Draw(img)
        for p in self.parts:
            px, py = self._pulled(p, t)
            color = p["c"]
            if self.gather_t is not None and t >= self.gather_t:
                if "target" not in p:                 # not needed: fade out
                    fade = max(0.0, 1 - (t - self.gather_t))
                    color = tuple(int(c * fade) for c in color)
                elif t >= p["release"]:               # let go: fly to its place
                    a = smooth((t - p["release"]) / self.travel)
                    sx, sy = self._pulled(p, p["release"])
                    tx, ty, tc = p["target"]
                    px, py = sx + (tx - sx) * a, sy + (ty - sy) * a
                    color = tuple(int(c0 + (c1 - c0) * a) for c0, c1 in zip(color, tc))
            if 0 <= px < self.width and 0 <= py < self.height:
                draw.point((x + px, y + py), fill=color)