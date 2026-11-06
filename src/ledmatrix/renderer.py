"""Send finished frames to the LED panels."""
import os

from PIL import Image

from typing import Protocol
from ledmatrix.config import HardwareConfig

class Renderer(Protocol):
    """Anything that can show frames: the panels or the browser preview."""

    width: int
    height: int

    def show(self, image: Image.Image) -> None: ...
    def clear(self) -> None: ...
    
class MatrixRenderer:
    """Shows Pillow images on the panels via rpi-rgb-led-matrix."""

    def __init__(self, hw: HardwareConfig) -> None:
        # Imported here, so the rest of the project also works without the library
        from rgbmatrix import RGBMatrix, RGBMatrixOptions

        options = RGBMatrixOptions()
        options.rows = hw.rows
        options.cols = hw.cols
        options.chain_length = hw.chain_length
        options.parallel = hw.parallel
        options.hardware_mapping = hw.hardware_mapping
        options.gpio_slowdown = hw.gpio_slowdown
        options.led_rgb_sequence = hw.rgb_sequence
        options.brightness = hw.brightness
        
        # After start the library gives up its root rights. Started with sudo, it
        # becomes the user who called sudo (instead of "daemon"), so the program
        # can still read your files - and later save the config.
        user = os.environ.get("SUDO_USER")
        if user:
            import grp, pwd   # only on Linux, that is why they are imported here
            options.drop_priv_user = user
            options.drop_priv_group = grp.getgrgid(pwd.getpwnam(user).pw_gid).gr_name

        self._matrix = RGBMatrix(options=options)
        self._canvas = self._matrix.CreateFrameCanvas()
        self.width = hw.width
        self.height = hw.height

    def show(self, image: Image.Image) -> None:
        """Display one frame."""
        self._canvas.SetImage(image.convert("RGB"))
        self._canvas = self._matrix.SwapOnVSync(self._canvas)

    def clear(self) -> None:
        """Turn all pixels off."""
        self._matrix.Clear()