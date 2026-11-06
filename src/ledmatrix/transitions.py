"""Transitions: blend from one finished frame to another."""

from typing import Callable

from PIL import Image

Transition = Callable[[Image.Image, Image.Image, float], Image.Image]


def fade(a: Image.Image, b: Image.Image, p: float) -> Image.Image:
    """a slowly turns into b (p = 0: only a, p = 1: only b)."""
    return Image.blend(a, b, max(0.0, min(1.0, p)))


def fade_black(a: Image.Image, b: Image.Image, p: float) -> Image.Image:
    """a goes dark, then b comes out of the dark."""
    p = max(0.0, min(1.0, p))
    black = Image.new("RGB", a.size)
    if p < 0.5:
        return Image.blend(a, black, p * 2)
    return Image.blend(black, b, (p - 0.5) * 2)


# name in config.yaml -> function
TRANSITIONS: dict[str, Transition] = {
    "fade": fade,
    "fade_black": fade_black,
}


def get(name: str) -> Transition:
    """The transition with this name, with a clear error for unknown names."""
    if name not in TRANSITIONS:
        known = ", ".join(TRANSITIONS)
        raise ValueError(f"Unknown transition '{name}'. Known: {known}")
    return TRANSITIONS[name]