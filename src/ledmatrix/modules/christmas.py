"""Christmas countdown with garland, tree and falling snow."""

import math
from ledmatrix.widgets.snow import Snow
from datetime import datetime, timedelta

from PIL import Image, ImageDraw

from ledmatrix.fonts import fit_font
from ledmatrix.modules.base import Module

BULB_COLORS = [(255, 40, 40), (40, 220, 60), (255, 190, 0), (40, 120, 255), (230, 60, 230)]


class Christmas(Module):
    """Counts down to Christmas Eve, then wishes a merry Christmas."""

    texts = {
        "en": {"title": "Christmas in", "days": "days", "day": "day", "done": "Merry Christmas!"},
        "de": {"title": "Weihnachten in", "days": "Tagen", "day": "Tag", "done": "Frohe Weihnachten!"},
        "fr": {"title": "Noël dans", "days": "jours", "day": "jour", "done": "Joyeux Noël !"},
        "es": {"title": "Navidad en", "days": "días", "day": "día", "done": "¡Feliz Navidad!"},
    }

    def __init__(self, width: int, height: int,
                 hour: int = 0,
                 snow: int = 40,
                 **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        self.title = self.text("title")
        self.days_label = self.text("days")
        self.day_label = self.text("day")
        self.done_text = self.text("done")
        self.hour = hour
        self.snow = Snow(width, height, count=snow)

        # the tree takes the left part, but only if the display is wide enough
        self.tree_w = int(height * 0.45) if width >= height * 1.5 else 0
        self.text_x = self.tree_w + 2
        text_w = width - self.text_x - 2

        # three text rows: title, days, time
        top = max(8, height // 8)  # room for the garland
        rows = height - top
        self.title_font = fit_font(self.title, text_w, rows // 5)
        self.days_font = fit_font("000 " + self.days_label, text_w, rows // 2)
        self.time_font = fit_font("00:00:00", text_w, rows // 4)
        self.done_font = fit_font(self.done_text, text_w, rows // 3)
        self.rows_top = top

    def start(self) -> None:
        self.snow.start()

    # ---------- time ----------

    def _target(self, now: datetime) -> datetime:
        """Christmas Eve of this year, or next year once Christmas is over."""
        target = datetime(now.year, 12, 24, self.hour)
        if now >= target + timedelta(days=3):
            target = datetime(now.year + 1, 12, 24, self.hour)
        return target

    # ---------- drawing ----------

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)

        self.snow.draw(img, 0, 0, t)
        self._draw_garland(draw, t)
        if self.tree_w:
            self._draw_tree(draw, t)

        now = datetime.now()
        left = self._target(now) - now
        if left.total_seconds() > 0:
            self._draw_countdown(draw, left)
        else:
            self._draw_done(draw, t)
        return img

    def _draw_garland(self, draw: ImageDraw.ImageDraw, t: float) -> None:
        span = 16  # distance between two hooks
        sag = max(2, self.rows_top // 2)
        wire = [(x, 1 + sag * math.sin(math.pi * (x % span) / span)) for x in range(self.width)]
        draw.line(wire, fill=(20, 70, 20))
        for i, x in enumerate(range(span // 2, self.width, span // 2)):
            y = 1 + sag * math.sin(math.pi * (x % span) / span)
            glow = 0.55 + 0.45 * math.sin(t * 3 + i * 1.7)
            r, g, b = BULB_COLORS[i % len(BULB_COLORS)]
            color = (int(r * glow), int(g * glow), int(b * glow))
            draw.rectangle((x - 1, y + 1, x, y + 2), fill=color)

    def _draw_tree(self, draw: ImageDraw.ImageDraw, t: float) -> None:
        cx = self.tree_w // 2 + 1
        top = self.rows_top + 4
        bottom = self.height - 6
        tiers = 3
        tier_h = (bottom - top) // tiers
        for i in range(tiers):
            y0 = top + i * tier_h - (2 if i else 0)
            half = 3 + (i + 1) * (self.tree_w // 2 - 3) // tiers
            draw.polygon([(cx, y0), (cx - half, y0 + tier_h + 2), (cx + half, y0 + tier_h + 2)],
                         fill=(0, 110 - i * 15, 30))
        # trunk
        draw.rectangle((cx - 2, bottom + 2, cx + 1, self.height - 2), fill=(110, 60, 20))
        # star
        pulse = 0.6 + 0.4 * math.sin(t * 4)
        star = (int(255 * pulse), int(210 * pulse), 0)
        draw.line((cx - 2, top - 1, cx + 2, top - 1), fill=star)
        draw.line((cx, top - 3, cx, top + 1), fill=star)
        # ornaments
        for i, (dx, dy) in enumerate([(-2, 0.3), (3, 0.45), (-4, 0.62), (4, 0.78), (0, 0.9), (-6, 0.95)]):
            y = top + int(dy * (bottom - top))
            on = math.sin(t * 2.5 + i * 2.1) > -0.3
            if on:
                draw.point((cx + dx, y), fill=BULB_COLORS[i % len(BULB_COLORS)])

    def _draw_countdown(self, draw: ImageDraw.ImageDraw, left: timedelta) -> None:
        cx = self.text_x + (self.width - self.text_x) / 2
        rows = self.height - self.rows_top
        hours, rest = divmod(left.seconds, 3600)
        minutes, seconds = divmod(rest, 60)

        draw.text((cx, self.rows_top + rows * 0.12), self.title, font=self.title_font,
                  fill=(255, 190, 0), anchor="mm")
        label = self.day_label if left.days == 1 else self.days_label
        draw.text((cx, self.rows_top + rows * 0.5), f"{left.days} {label}",
                  font=self.days_font, fill=(255, 40, 40), anchor="mm")
        draw.text((cx, self.rows_top + rows * 0.86), f"{hours:02}:{minutes:02}:{seconds:02}",
                  font=self.time_font, fill=(230, 230, 230), anchor="mm")

    def _draw_done(self, draw: ImageDraw.ImageDraw, t: float) -> None:
        cx = self.text_x + (self.width - self.text_x) / 2
        cy = self.rows_top + (self.height - self.rows_top) / 2
        # every letter in its own color, colors run through the text
        x = cx - self.done_font.getlength(self.done_text) / 2
        for i, char in enumerate(self.done_text):
            color = BULB_COLORS[(i + int(t * 6)) % len(BULB_COLORS)]
            draw.text((x, cy), char, font=self.done_font, fill=color, anchor="lm")
            x += self.done_font.getlength(char)