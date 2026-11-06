"""Animated GIF widget."""

from pathlib import Path

from PIL import Image, ImageSequence

from ledmatrix.widgets.base import Widget


class Gif(Widget):
    """Plays an animated GIF (or shows a still image), scaled into its area."""

    def __init__(self, width: int, height: int, path: str | Path,
                 fit: str = "contain", speed: float = 1.0) -> None:
        super().__init__(width, height)
        self.frames: list[Image.Image] = []
        self.times: list[float] = []  # start time of every frame in seconds

        # load all frames once and scale them, so playing is cheap
        total = 0.0
        with Image.open(path) as gif:
            for frame in ImageSequence.Iterator(gif):
                self.times.append(total)
                self.frames.append(self._scale(frame.convert("RGBA"), fit))
                total += frame.info.get("duration", 100) / 1000 / speed
        self.length = max(total, 0.01)  # seconds for one run of the animation

    def _scale(self, frame: Image.Image, fit: str) -> Image.Image:
        """Scale a frame into the widget area and center it."""
        if fit == "stretch":
            return frame.resize((self.width, self.height), Image.LANCZOS)
        ratio_w = self.width / frame.width
        ratio_h = self.height / frame.height
        ratio = max(ratio_w, ratio_h) if fit == "cover" else min(ratio_w, ratio_h)
        size = (max(1, round(frame.width * ratio)), max(1, round(frame.height * ratio)))
        scaled = frame.resize(size, Image.LANCZOS)
        canvas = Image.new("RGBA", (self.width, self.height))
        canvas.paste(scaled, ((self.width - size[0]) // 2, (self.height - size[1]) // 2))
        return canvas

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        # find the frame that belongs to time t
        now = t % self.length
        index = 0
        while index + 1 < len(self.times) and self.times[index + 1] <= now:
            index += 1
        frame = self.frames[index]
        # the alpha channel keeps transparent parts of the GIF see-through
        img.paste(frame, (x, y), frame)