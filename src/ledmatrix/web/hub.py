"""Keeps the latest frame for the web interface and passes every frame on."""

import threading

from PIL import Image

from ledmatrix.renderer import Renderer


class FrameHub:
    """Sits in front of a renderer: every frame goes on to it (if there is one),
    and a copy stays here for the browser."""

    def __init__(self, width: int, height: int, target: Renderer | None = None) -> None:
        self.width = width
        self.height = height
        self.target = target            # the panels, or None in the preview
        self._lock = threading.Lock()
        self._frame = bytes(width * height * 3)
        self._frame_id = 0

    def show(self, image: Image.Image) -> None:
        if self.target is not None:
            self.target.show(image)
        data = image.convert("RGB").tobytes()
        with self._lock:
            self._frame = data
            self._frame_id += 1

    def clear(self) -> None:
        if self.target is not None:
            self.target.clear()
        with self._lock:
            self._frame = bytes(self.width * self.height * 3)
            self._frame_id += 1

    def latest(self) -> tuple[int, bytes]:
        """Number and raw RGB bytes of the newest frame."""
        with self._lock:
            return self._frame_id, self._frame