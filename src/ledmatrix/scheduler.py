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

    def run(self) -> None:
        """Loop forever (stop with Ctrl+C)."""
        index = 0
        while True:
            module = self.modules[index]
            module.start()
            start = time.monotonic()

            while (t := time.monotonic() - start) < module.duration:
                frame_start = time.monotonic()
                self.renderer.show(module.render(t))
                # wait for the rest of the frame, so we get a steady frame rate
                rest = self.frame_time - (time.monotonic() - frame_start)
                if rest > 0:
                    time.sleep(rest)

            index = (index + 1) % len(self.modules)