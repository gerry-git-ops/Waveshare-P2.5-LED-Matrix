"""Font helpers shared by all modules."""

import io
from functools import lru_cache
from importlib import resources

from PIL import ImageDraw, ImageFont

# bundled font: Inter (SIL Open Font License, see assets/fonts/OFL.txt)
FONT_DATA = (resources.files("ledmatrix")
             .joinpath("assets/fonts/Inter-SemiBold.otf").read_bytes())


@lru_cache(maxsize=64)
def font(size: int) -> ImageFont.FreeTypeFont:
    """The project font in the given size (cached)."""
    return ImageFont.truetype(io.BytesIO(FONT_DATA), size)


def fit_font(text: str, max_width: int, max_height: int,
             fixed: bool = False) -> ImageFont.FreeTypeFont:
    """Largest font in which the text fits into max_width x max_height.

    fixed=True measures the width like draw_fixed() draws it.
    """
    size = max_height
    while size > 6:
        f = font(size)
        left, top, right, bottom = f.getbbox(text)
        width = fixed_length(text, f) if fixed else right - left
        if width <= max_width and bottom - top <= max_height:
            return f
        size -= 1
    return font(6)

def digit_width(f: ImageFont.FreeTypeFont) -> float:
    """Width of the widest digit, used as the same width for every digit."""
    return max(f.getlength(c) for c in "0123456789")


def fixed_length(text: str, f: ImageFont.FreeTypeFont) -> float:
    """Width of the text if every digit gets the same width."""
    w = digit_width(f)
    return sum(w if c.isdigit() else f.getlength(c) for c in text)


def draw_fixed(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str,
               f: ImageFont.FreeTypeFont, fill: tuple[int, int, int]) -> None:
    """Draw text centered at xy, every digit in a cell of the same width.

    Numbers like a clock then keep their position instead of jumping around.
    """
    w = digit_width(f)
    x = xy[0] - fixed_length(text, f) / 2
    for c in text:
        cell = w if c.isdigit() else f.getlength(c)
        draw.text((x + cell / 2, xy[1]), c, font=f, fill=fill, anchor="mm")
        x += cell