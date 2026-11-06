"""Color palettes shared by all modules."""

import colorsys

Color = tuple[int, int, int]

# palette name -> hue in degrees on the color wheel
HUES = {
    "red": 0, "orange": 25, "gold": 45, "green": 125,
    "cyan": 185, "blue": 210, "purple": 275, "pink": 325,
}


def shade(hue: float, saturation: float, value: float = 1.0) -> Color:
    """One color of the given hue: saturation 0 = white, 1 = full color."""
    r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
    return int(r * 255), int(g * 255), int(b * 255)


def palette(name: str) -> dict[str, Color]:
    """Four matching colors of one hue, from strong to almost white."""
    if name not in HUES:
        known = ", ".join(HUES)
        raise ValueError(f"Unknown palette '{name}'. Known: {known}")
    hue = HUES[name]
    return {
        "strong": shade(hue, 0.70),
        "light": shade(hue, 0.42),
        "soft": shade(hue, 0.26, 0.92),
        "pale": shade(hue, 0.16),
    }