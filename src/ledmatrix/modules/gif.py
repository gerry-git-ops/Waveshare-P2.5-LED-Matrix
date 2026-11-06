"""Play an animated GIF on the display."""

from PIL import Image

from ledmatrix.modules.base import Module
from ledmatrix.widgets.media.gif import Gif


class GifPlayer(Module):
    """Shows an animated GIF over the whole display."""

    def __init__(self, width: int, height: int,
                 file: str = "",
                 fit: str = "contain",
                 speed: float = 1.0,
                 loops: int = 1,
                 **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        if not file:
            raise ValueError("The gif module needs a 'file'")
        self.gif = Gif(width, height, file, fit=fit, speed=speed)
        self.duration = loops * self.gif.length

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        self.gif.draw(img, 0, 0, t)
        return img