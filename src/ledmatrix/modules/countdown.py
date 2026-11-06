"""Countdown to any date and time."""

from datetime import date, datetime

from PIL import Image, ImageDraw

from ledmatrix.fonts import fit_font
from ledmatrix.modules.base import Module
from ledmatrix.widgets.countdown import Countdown


def to_datetime(value: str | date | datetime) -> datetime:
    """Accept "2027-05-01", "2027-05-01 18:00" or a YAML date/timestamp."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    return datetime.fromisoformat(str(value))


class CountdownModule(Module):
    """Title on top, days and time left below, a message once the moment is reached."""

    texts = {
        "en": {"title": "Only", "day": "day", "days": "days", "done": "It's time!"},
        "de": {"title": "Noch", "day": "Tag", "days": "Tage", "done": "Es ist so weit!"},
        "fr": {"title": "Encore", "day": "jour", "days": "jours", "done": "C'est le moment !"},
        "es": {"title": "Faltan", "day": "día", "days": "días", "done": "¡Ha llegado el día!"},
    }

    def __init__(self, width: int, height: int,
                 date: str | date | datetime,
                 title_color: tuple[int, int, int] = (255, 190, 0),
                 days_color: tuple[int, int, int] = (255, 40, 40),
                 time_color: tuple[int, int, int] = (230, 230, 230),
                 **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        self.title = self.text("title")
        self.done_text = self.text("done")
        self.title_color = tuple(title_color)

        # title gets the top quarter, the countdown the rest
        self.title_h = height // 4
        self.title_font = fit_font(self.title, width - 4, self.title_h)
        self.done_font = fit_font(self.done_text, width - 4, height // 3)
        self.countdown = Countdown(width - 4, height - self.title_h, to_datetime(date),
                                   day=self.text("day"), days=self.text("days"),
                                   days_color=days_color, time_color=time_color)

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        cx = self.width / 2

        if self.countdown.left().total_seconds() > 0:
            draw.text((cx, self.title_h / 2), self.title, font=self.title_font,
                      fill=self.title_color, anchor="mm")
            self.countdown.draw(img, 2, self.title_h, t)
        else:
            draw.text((cx, self.height / 2), self.done_text, font=self.done_font,
                      fill=self.title_color, anchor="mm")
        return img