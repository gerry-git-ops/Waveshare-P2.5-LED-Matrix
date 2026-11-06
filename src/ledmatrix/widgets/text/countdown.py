"""Countdown widget: days and time left until a moment."""

from datetime import datetime, timedelta

from PIL import Image, ImageDraw

from ledmatrix.fonts import draw_fixed, fit_font
from ledmatrix.widgets.base import Widget


class Countdown(Widget):
    """Shows "12 days" on top and "03:25:07" below it."""

    def __init__(self, width: int, height: int, target: datetime,
                 day: str = "day", days: str = "days",
                 days_color: tuple[int, int, int] = (255, 40, 40),
                 time_color: tuple[int, int, int] = (230, 230, 230)) -> None:
        super().__init__(width, height)
        self.target = target
        self.day = day
        self.days = days
        self.days_color = tuple(days_color)
        self.time_color = tuple(time_color)
        # days row gets two thirds of the height, time row one third
        self.days_font = fit_font("000 " + days, width, height * 2 // 3, fixed=True)
        self.time_font = fit_font("00:00:00", width, height // 3, fixed=True)

    def left(self) -> timedelta:
        """Time left until the target (negative once it is reached)."""
        return self.target - datetime.now()

    def draw(self, img: Image.Image, x: int, y: int, t: float) -> None:
        left = max(self.left(), timedelta(0))
        hours, rest = divmod(left.seconds, 3600)
        minutes, seconds = divmod(rest, 60)
        label = self.day if left.days == 1 else self.days

        draw = ImageDraw.Draw(img)
        cx = x + self.width / 2
        draw_fixed(draw, (cx, y + self.height * 0.33), f"{left.days} {label}",
                   self.days_font, self.days_color)
        draw_fixed(draw, (cx, y + self.height * 0.83), f"{hours:02}:{minutes:02}:{seconds:02}",
                   self.time_font, self.time_color)