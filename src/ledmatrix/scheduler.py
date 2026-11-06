"""Play modules one after another."""

import time

from ledmatrix.modules.base import Module
from ledmatrix.renderer import Renderer


class Scheduler:
    """Shows each module for its duration, then switches to the next."""

    def __init__(self, renderer: Renderer, modules: list[Module],
                 fps: int = 30) -> None:
        if not modules:
            raise ValueError("At least one enabled module is required")
        self.renderer = renderer
        self.modules = modules
        self.frame_time = 1 / fps
                # what is on screen right now, read by the web interface
        self.index = 0
        self.started = time.monotonic()
        self.fps = 0.0

    def status(self) -> dict:
        """The module on screen, how long it has been running and the real frame rate."""
        module = self.modules[self.index]
        elapsed = time.monotonic() - self.started
        return {
            "module": module.name,
            "config_index": module.config_index,
            "elapsed": round(elapsed, 1),
            "remaining": round(max(0.0, module.duration - elapsed), 1),
            "duration": round(module.duration, 1),
            "fps": round(self.fps, 1),
        }

    def run(self) -> None:
        """Loop forever (stop with Ctrl+C)."""
        while True:
            module = self.modules[self.index]
            module.start()
            self.started = start = time.monotonic()
            last = start

            while (t := time.monotonic() - start) < module.duration:
                frame_start = time.monotonic()
                self.renderer.show(module.render(t))
                # wait for the rest of the frame, so we get a steady frame rate
                rest = self.frame_time - (time.monotonic() - frame_start)
                if rest > 0:
                    time.sleep(rest)
                # real frame rate, smoothed so the number does not jump around
                now = time.monotonic()
                self.fps = 0.9 * self.fps + 0.1 / max(now - last, 1e-6)
                last = now

            self.index = (self.index + 1) % len(self.modules)