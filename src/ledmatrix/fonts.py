"""Font helpers shared by all modules."""

import io
from functools import lru_cache
from importlib import resources

from PIL import ImageFont

# bundled font: Inter (SIL Open Font License, see assets/fonts/OFL.txt)
FONT_DATA = (resources.files("ledmatrix")
             .joinpath("assets/fonts/Inter-SemiBold.otf").read_bytes())


@lru_cache(maxsize=64)
def font(size: int) -> ImageFont.FreeTypeFont:
    """The project font in the given size (cached)."""
    return ImageFont.truetype(io.BytesIO(FONT_DATA), size)


def fit_font(text: str, max_width: int, max_height: int) -> ImageFont.FreeTypeFont:
    """Largest font in which the text fits into max_width x max_height."""
    size = max_height
    while size > 6:
        f = font(size)
        left, top, right, bottom = f.getbbox(text)
        if right - left <= max_width and bottom - top <= max_height:
            return f
        size -= 1
    return font(6)