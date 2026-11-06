"""Voyage countdown: a ship crashes into the time and drags the trip details into place."""

from datetime import date, datetime

from PIL import Image, ImageDraw, ImageFilter

from ledmatrix import colors, transitions
from ledmatrix.fonts import fit_font
from ledmatrix.modules.base import Module
from ledmatrix.modules.countdown import CountdownModule, to_datetime
from ledmatrix.widgets.effects.particles import Particles
from ledmatrix.widgets.scenery.sky import Sky
from ledmatrix.widgets.scenery.water import Water
from ledmatrix.widgets.text.countdown import Countdown
from ledmatrix.widgets.media.gif import Gif

Color = colors.Color


class Voyage(Module):
    """Countdown on the sea. A ship comes closer, crashes into the time,
    and the pixels are dragged along behind it into the lines of your trip."""

    # title, day and days come from the countdown module, "trip" is the default end line
    texts = {
        "en": {**CountdownModule.texts["en"], "trip": "Bon voyage!"},
        "de": {**CountdownModule.texts["de"], "trip": "Gute Reise!"},
        "fr": {**CountdownModule.texts["fr"], "trip": "Bon voyage !"},
        "es": {**CountdownModule.texts["es"], "trip": "¡Buen viaje!"},
    }

    def __init__(self, width: int, height: int,
                 date: str | date | datetime,
                 lines: list[str] | None = None,
                 ship: str = "examples/cruise_ship.png",
                 ship_speed: float = 1.0,
                 hold: float = 6.0,
                 palette: str = "blue",
                 title_color: Color | None = None,
                 days_color: Color | None = None,
                 time_color: Color | None = None,
                 line_colors: list[Color] | None = None,
                 finale: list[dict] | None = None,
                 transition: str = "fade",
                 transition_time: float = 1.5,
                 **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        if ship_speed <= 0:
            raise ValueError("ship_speed must be greater than 0")

        # timeline in seconds: the ship part gets shorter with a faster ship,
        # the trip lines stay 'hold' seconds once they are complete
        self.ship_in = 1.5
        self.impact = self.ship_in + 2.8 / ship_speed
        self.ship_out = self.ship_in + 6.5 / ship_speed
        self.duration = self.ship_out + 1.5 + hold

        # colors: the palette gives all of them, single colors from the config win
        p = colors.palette(palette)
        self.title_color = tuple(title_color or p["light"])
        days_color = tuple(days_color or p["strong"])
        time_color = tuple(time_color or p["pale"])
        self.line_colors = [tuple(c) for c in
                            line_colors or [p["pale"], p["strong"], p["light"], p["soft"]]]

        # dark background, so the text stands out on the LEDs
        self.horizon = int(height * 0.72)
        self.sky = Sky(width, self.horizon, top=(2, 4, 14), bottom=(8, 20, 52))
        self.water = Water(width, height - self.horizon, back=(2, 12, 34), front=(4, 18, 44))
        self.ship = Image.open(ship).convert("RGBA")
        self.particles = Particles(width, height)

        # countdown: title in the top sixth, days and time below
        title = self.text("title")
        self.title_h = height // 6
        self.title_font = fit_font(title, width - 4, self.title_h)
        self.title = title
        self.countdown = Countdown(width - 4, int(height * 0.58), to_datetime(date),
                                   day=self.text("day"), days=self.text("days"),
                                   days_color=days_color, time_color=time_color)
        self.lines = self._lines_image(lines or [self.text("trip")])
        self.lines_halo = self._halo(self.lines)
        # finale: GIFs or pictures after the trip lines, each one blends into the next.
        # every part stays fully visible for its time, the blending comes on top
        self.blend = transitions.get(transition)
        self.blend_time = transition_time
        self.finale: list[tuple[float, float, Gif, bool]] = []   # start, length, picture, play once
        end = self.duration                                      # end of the trip lines
        for item in finale or []:
            unknown = set(item) - {"file", "fit", "hold"}
            if unknown:
                raise ValueError(f"Unknown finale option(s): {', '.join(sorted(unknown))}. "
                                 "Allowed: file, fit, hold")
            gif = Gif(width, height, item["file"], fit=item.get("fit", "contain"))
            animated = len(gif.frames) > 1
            once = animated and "hold" not in item                # a clip without hold runs once
            length = gif.length if once else item.get("hold", 3.0)
            start = end                                           # blending in starts here
            self.finale.append((start, length, gif, once))
            end = start + transition_time + length                # then fully visible for 'length' s
        self.duration = end

    # ---------- pictures ----------

    def _countdown_image(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        draw.text((self.width / 2, self.title_h / 2 + 1), self.title, font=self.title_font,
                  fill=self.title_color, anchor="mm")
        self.countdown.draw(img, 2, self.title_h, 0)
        return img

    def _lines_image(self, lines: list[str]) -> Image.Image:
        """The trip lines, one below the other, each as big as fits."""
        img = Image.new("RGB", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        slot = (self.height - 4) / len(lines)
        for i, line in enumerate(lines):
            font = fit_font(line, self.width - 4, int(slot * 0.75))
            draw.text((self.width / 2, 2 + slot * (i + 0.5)), line, font=font,
                      fill=self.line_colors[i % len(self.line_colors)], anchor="mm")
        return img

    # ---------- ship ----------

    def _ship_state(self, t: float) -> tuple[float, float, float]:
        """Bottom center x, bottom y and width of the ship at time t."""
        a = max(0.0, min(1.0, (t - self.ship_in) / (self.ship_out - self.ship_in)))
        size = self.width * (0.04 + 1.25 * a ** 2)     # small far away, fast growing near us
        x = self.width * (0.81 - 1.64 * a ** 1.9)      # from the right to far out on the left
        y = self.horizon + 2 + self.height * 0.63 * a ** 2
        return x, y, size

    def _stern(self, t: float) -> tuple[float, float]:
        """The point that pulls the pixels along: right side of the ship."""
        x, y, w = self._ship_state(t)
        return x + w * 0.45, y - w * 0.35

    def _release(self, column: float) -> float:
        """First moment the right side of the ship has passed this column."""
        t = self.impact + 1.0
        while t < self.ship_out - 0.3 and self._stern(t)[0] >= column:
            t += 0.02
        return t

    def _draw_ship(self, img: Image.Image, t: float) -> None:
        x, y, w = self._ship_state(t)
        w = max(2, int(w))
        h = max(2, int(self.ship.height * w / self.ship.width))
        sprite = self.ship.resize((w, h), Image.LANCZOS)
        img.paste(sprite, (int(x - w / 2), int(y - h)), sprite)

    # ---------- module ----------

    def start(self) -> None:
        self.sky.start()
        x, y, w = self._ship_state(self.impact)
        self.impact_point = (x, y - w * 0.6)
        self.crashed = False

    def _crash(self) -> None:
        """The time on screen at this moment bursts apart and is gathered into the lines."""
        self.particles.burst(self._countdown_image(), self.impact_point, self.impact)
        # release time for every column, worked out once instead of for every single pixel
        release = [self._release(x) for x in range(self.width)]
        self.particles.gather(self.lines, self.impact + 0.6, attractor=self._stern,
                              release=lambda x: release[int(x)])
        self.crashed = True

    @staticmethod
    def _halo(text_img: Image.Image) -> Image.Image:
        """Mask a bit bigger than the text: drawn dark behind it, it gives the text an outline."""
        lit = text_img.convert("L").point(lambda v: 255 if v > 40 else 0)
        return lit.filter(ImageFilter.MaxFilter(3))

    def _finale_frame(self, index: int, t: float) -> Image.Image:
        start, length, gif, once = self.finale[index]
        local = max(0.0, t - start - self.blend_time)             # first frame while blending in
        if once:
            local = min(local, gif.length - 0.001)                # stop on the last frame
        img = Image.new("RGB", (self.width, self.height))
        gif.draw(img, 0, 0, local)
        return img

    def render(self, t: float) -> Image.Image:
        # the last part that has started: -1 is the ship scene, 0.. the finale pictures
        index = -1
        for i, (start, *_rest) in enumerate(self.finale):
            if t >= start:
                index = i
        if index == -1:
            return self._scene(t)

        frame = self._finale_frame(index, t)
        start = self.finale[index][0]
        if t < start + self.blend_time:                           # still blending in
            before = self._scene(t) if index == 0 else self._finale_frame(index - 1, t)
            frame = self.blend(before, frame, (t - start) / self.blend_time)
        return frame

    def _scene(self, t: float) -> Image.Image:
        """Sea, sky, ship, countdown and the trip lines."""
        img = Image.new("RGB", (self.width, self.height))
        self.sky.draw(img, 0, 0, t)
        self.water.draw(img, 0, self.horizon, t)

        if t < self.impact:
            if t >= self.ship_in:
                self._draw_ship(img, t)               # still behind the time
            live = self._countdown_image()
            img.paste((0, 0, 0), mask=self._halo(live))
            img.paste(live, mask=live.convert("L").point(lambda v: 255 if v > 40 else 0))
            return img

        if not self.crashed:
            self._crash()
        dt = t - self.impact
        if dt < 0.25:                                 # short flash ring at the impact
            r, v = 4 + dt * 60, int(255 * (1 - dt / 0.25))
            ix, iy = self.impact_point
            ImageDraw.Draw(img).ellipse((ix - r, iy - r, ix + r, iy + r), outline=(v, v, v))
        # the dark outline of the lines fades in while the pixels arrive
        fade = max(0.0, min(1.0, (t - self.ship_out + 1.0) / 2.0))
        if fade > 0:
            img.paste((0, 0, 0), mask=self.lines_halo.point(lambda v: int(v * fade)))
        self.particles.draw(img, 0, 0, t)
        if t < self.ship_out:
            self._draw_ship(img, t)                   # now in front
        return img