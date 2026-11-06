**English** | [Deutsch](/docs/README.de.md)

<div align="center">

# ✦ Waveshare P2.5 LED Matrix

**A modular display system for HUB75 LED panels on the Raspberry Pi.**<br>
Build your own modules – clocks, countdowns, crypto tickers, animations – and let them run seamlessly one after another.

![Raspberry Pi 4](https://img.shields.io/badge/Raspberry%20Pi-4-C51A4A?logo=raspberrypi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Panels](https://img.shields.io/badge/Panels-4%C3%97%2064%C3%9732-00b4d8)
![Status](https://img.shields.io/badge/Status-work%20in%20progress-orange)
![License](https://img.shields.io/badge/License-GPL--3.0-blue)
![Languages](https://img.shields.io/badge/Languages-EN%20%C2%B7%20DE%20%C2%B7%20FR%20%C2%B7%20ES-8a2be2)

<img src="docs/images/playlist.gif" width="100%" alt="The matrix playing the Christmas countdown and two clocks one after another">

<sub>Real panels, real time: the Christmas countdown and two clock styles playing one after another.</sub>

</div>

---

## 🎄 Seasonal highlight: Christmas countdown

Get your matrix into the holiday mood: a twinkling garland, a tree with a glowing star,
gently falling snow – and a big countdown to Christmas Eve. On Christmas Eve it switches
to a colorful greeting, and after the holidays it starts counting towards the next Christmas by itself.

<div align="center">
<img src="docs/images/christmas.gif" width="100%" alt="Animated Christmas countdown on the LED matrix">
</div>

It speaks your language – English, German, French and Spanish are built in:

<div align="center">
<img src="docs/images/christmas-en.jpg" width="49%" alt="Christmas countdown in English">
<img src="docs/images/christmas-de.jpg" width="49%" alt="Christmas countdown in German">
<img src="docs/images/christmas-fr.jpg" width="49%" alt="Christmas countdown in French">
<img src="docs/images/christmas-es.jpg" width="49%" alt="Christmas countdown in Spanish">
</div>

Add it to your `config/config.yaml`:

```yaml
language: de                # en, de, fr, es

modules:
  - type: christmas
    duration: 15
    hour: 18                # Christmas Eve at 18:00, 0 = midnight
    snow: 40                # number of snowflakes, 0 = no snow
```

Your own words? Every text can be replaced right in the config – see [Languages](#-languages).

---

## ✦ Idea

Not a single script, but a small platform: the system takes care of hardware,
timing and playback. You only write **modules** that define *what* is shown.
Everything that depends on your hardware lives in one config file – so the same code
runs on any panel size, chain length or wiring.

## ✦ Architecture

```mermaid
flowchart LR
    A[Modules<br/>Clock · Countdown · Crypto · GIF …] --> B[Scheduler<br/>order & duration]
    E[config.yaml] --> A
    E --> B
    B --> C{Renderer}
    C --> D[LED panels<br/>via rpi-rgb-led-matrix]
    C --> F[Browser preview<br/>no hardware needed]
```

## ✦ Preview mode

Develop and test modules **without any panels** – the preview draws the matrix as
glowing LEDs in your browser, live at 30 fps.

<div align="center">
<img src="docs/images/preview.gif" width="100%" alt="Browser preview showing the clock modules">
</div>

- Adjustable size, LED size, glow and LED shape (round or square)
- Shows the pixel coordinate under the mouse – handy when building modules
- Screenshot button, fullscreen with <kbd>F</kbd>, hide the controls with <kbd>H</kbd>
- Runs on the Pi as well as on any PC with Python

---

## ✦ Quick start

Tested on a Raspberry Pi 4 with Raspberry Pi OS Lite (64-bit), Python 3.13.

### 1 · System packages

```bash
sudo apt update
sudo apt install -y git build-essential python3-dev python3-venv cython3
```

### 2 · Disable the on-board sound

The built-in sound of the Pi uses the same hardware as the LED library and causes trouble.

```bash
echo "blacklist snd_bcm2835" | sudo tee /etc/modprobe.d/blacklist-rgb-matrix.conf
sudo reboot
```

### 3 · Get the code

```bash
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
git clone https://github.com/gerry-git-ops/Waveshare-P2.5-LED-Matrix.git
cd Waveshare-P2.5-LED-Matrix
```

### 4 · Virtual environment and installation

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

pip install ~/rpi-rgb-led-matrix   # Python bindings of the LED library (takes a few minutes)
pip install -e .                   # this project
```

### 5 · Configuration

```bash
cp config/config.example.yaml config/config.yaml
```

Adjust `config/config.yaml` to your panels – see [Configuration](#-configuration).

### 6 · Run

```bash
sudo .venv/bin/python -m ledmatrix          # on the LED panels (needs root for GPIO)
python -m ledmatrix --preview               # in the browser: http://localhost:8080
```

Stop with <kbd>Ctrl</kbd>+<kbd>C</kbd>.

> [!TIP]
> Working on the Pi over **VS Code Remote-SSH**? VS Code forwards port 8080 automatically –
> just click *Open in Browser*. With plain SSH: `ssh -L 8080:localhost:8080 user@your-pi`

<details>
<summary><b>Preview on a PC (Windows, macOS, Linux) – no Pi needed</b></summary>

<br>

You need Python 3.11 or newer. The LED library is **not** required for the preview.

```bash
git clone https://github.com/gerry-git-ops/Waveshare-P2.5-LED-Matrix.git
cd Waveshare-P2.5-LED-Matrix
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
cp config/config.example.yaml config/config.yaml   # Windows: copy config\config.example.yaml config\config.yaml
python -m ledmatrix --preview
```

Then open <http://localhost:8080>.

</details>

---

## ✦ Configuration

All settings live in `config/config.yaml`. Your own file is ignored by Git,
the template `config.example.yaml` is part of the repository.

```yaml
hardware:
  rows: 32                  # pixel rows per panel
  cols: 64                  # pixel columns per panel
  chain_length: 2           # panels per chain
  parallel: 2               # parallel chains (1-3)
  hardware_mapping: regular # GPIO mapping, see rpi-rgb-led-matrix
  gpio_slowdown: 4          # higher = slower, needed on faster Pis
  rgb_sequence: RBG         # color order of your panels
  brightness: 50            # 0-100

fps: 30                     # frames per second
language: en                # en, de, fr, es – missing texts fall back to English

modules:                    # played in this order, then from the start
  - type: clock
    duration: 5             # seconds
    color: [0, 150, 255]
    fmt: "%H:%M:%S"

  - type: christmas
    duration: 15
    hour: 18
```

The display size is calculated from the hardware section:
**width = `cols` × `chain_length`**, **height = `rows` × `parallel`** (here 128 × 64).

> [!IMPORTANT]
> The hardware section must match the panels that are **actually connected**.
> If it doesn't, panels show copies of the image or flicker.

Every module entry needs a `type`. Optional for every module:

| Key | Meaning |
|-----|---------|
| `enabled` | `false` switches the module off without deleting it (default: `true`) |
| `duration` | seconds on screen – if left out, the module decides itself (e.g. `scrolltext` by its loops) |

All other keys are handed to the module as options.

### ✦ Languages

`language` sets the language for all modules. Built in: **English** (`en`), **German** (`de`),
**French** (`fr`) and **Spanish** (`es`). If a text is missing in your language, English is used –
nothing breaks.

**Change single texts** directly in the config, no code needed. Just use the text key of the module:

```yaml
  - type: christmas
    title: "Only"           # instead of "Christmas in"
    done: "Ho ho ho!"       # instead of "Merry Christmas!"
```

| Module | Text keys |
|--------|-----------|
| `christmas` | `title`, `days`, `day`, `done` |
| `countdown` | `title`, `days`, `day`, `done` |
| `scrolltext` | `text` |

**Your language is missing?** Add it to the `texts` of the module (see
[Build your own module](#-build-your-own-module)) and open a pull request – contributions are very welcome.

## ✦ Modules

| Module | Description | Options | Status |
|--------|-------------|---------|--------|
| `clock` | Digital clock, scales itself to the display | `color`, `fmt` ([strftime](https://docs.python.org/3/library/time.html#time.strftime)) | ✅ |
| `christmas` | 🎄 Countdown to Christmas Eve with garland, tree and snow | `hour`, `snow`, [texts](#-languages) | ✅ |
| `scrolltext` | Scrolling text in one color or rainbow, runs a set number of times | `loops`, `speed`, `size`, `color`, `rainbow`, [`text`](#-languages) | ✅ |
| `countdown` | Days and time left until any date, with a message once it is reached | `date`, `title_color`, `days_color`, `time_color`, [texts](#-languages) | ✅ |
| `gif` | Plays an animated GIF a set number of times | `file`, `fit`, `speed`, `loops` | ✅ |
| Crypto ticker | Prices via web API, with history | | idea |

<div align="center">
<img src="docs/images/matrix-clock-blue.jpg" width="49%" alt="Clock module with seconds">
<img src="docs/images/matrix-clock-orange.jpg" width="49%" alt="Clock module without seconds">
<br><sub>The same <code>clock</code> module twice – only <code>color</code> and <code>fmt</code> differ.</sub>
</div>

<div align="center">
<img src="docs/images/scrolltext.gif" width="70%" alt="Scrolling rainbow text on the LED matrix">
<br><sub><code>scrolltext</code> with <code>rainbow: true</code> – it runs through completely <code>loops</code> times, then the next module follows.</sub>
</div>

```yaml
  - type: scrolltext
    loops: 2                # how often the text runs through completely
    speed: 40               # pixels per second
    size: 0.6               # text height, share of the display height
    rainbow: true           # or: color: [255, 255, 255]
    # text: "Your own text" # optional, replaces the translated default text
```

> [!NOTE]
> Leave out `duration` for `scrolltext` – otherwise it overrides the loops.

<div align="center">
<img src="docs/images/countdown-example.png" width="60%" alt="Countdown module on the LED matrix">
<br><sub><code>countdown</code> – title on top, days and time below. Once the date is reached, it shows the <code>done</code> text.</sub>
</div>

```yaml
  - type: countdown
    duration: 10
    date: "2027-01-01 00:00"  # "YYYY-MM-DD" or "YYYY-MM-DD HH:MM"
    title: "Holiday in"       # optional, replaces the translated title
    done: "Have fun!"         # optional, shown once the date is reached
```

<div align="center">
<img src="docs/images/gif-star.gif" width="60%" alt="Example GIF of a spinning star on the LED matrix">
<br><sub><code>gif</code> playing the included example <code>examples/star.gif</code> – original pixel art made for this project.</sub>
</div>

```yaml
  - type: gif
    file: examples/star.gif # path from the project folder
    fit: contain            # contain, cover or stretch
    speed: 1.0              # 2.0 = twice as fast
    loops: 3                # how often the animation plays completely
```

> [!NOTE]
> Only use GIFs you are allowed to use. Your own GIFs are best kept in the `private/` folder –
> it is ignored by Git.

## ✦ Widgets – building blocks

Modules don't have to start from scratch: **widgets** are small building blocks that each draw
*one thing* into an *area* you give them. A module just puts them together – back to front.

| Widget | Draws | Options |
|--------|-------|---------|
| `ScrollingText` | text moving from right to left | `text`, `color`, `rainbow`, `speed`, `size` |
| `Gif` | an animated GIF or a still image | `path`, `fit`, `speed` |
| `Snow` | falling snowflakes | `count`, `color` |
| `Countdown` | days and time left until a moment | `target`, `day`, `days`, `days_color`, `time_color` |

The built-in modules are made of them, too: `scrolltext` is one `ScrollingText`,
`gif` is one `Gif`, `countdown` is one `Countdown`, and `christmas` uses `Snow` and `Countdown`.

Example – a star with falling snow and a rainbow text in the bottom row:

```python
from PIL import Image

from ledmatrix.modules.base import Module
from ledmatrix.widgets.media.gif import Gif
from ledmatrix.widgets.text.scrolling_text import ScrollingText
from ledmatrix.widgets.effects.snow import Snow


class StarNight(Module):
    """A star with falling snow, and a scrolling text below."""

    texts = {
        "en": {"text": "Good night!"},
        "de": {"text": "Gute Nacht!"},
    }

    def __init__(self, width: int, height: int, **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        text_h = height // 4                       # bottom quarter for the text
        self.snow = Snow(width, height - text_h, count=30)
        self.star = Gif(width, height - text_h, "examples/star.gif")
        self.scroller = ScrollingText(width, text_h, self.text("text"), rainbow=True, size=0.8)
        self.duration = 2 * self.scroller.pass_time()  # two runs of the text

    def start(self) -> None:
        self.snow.start()

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        text_y = self.height - self.scroller.height
        self.star.draw(img, 0, 0, t)               # back
        self.snow.draw(img, 0, 0, t)               # middle
        self.scroller.draw(img, 0, text_y, t)          # bottom row
        return img
```

<div align="center">
<img src="docs/images/widgets-example.png" width="60%" alt="Star, snow and scrolling text combined in one module">
</div>

`draw(img, x, y, t)` paints the widget at position `x, y`, every widget only within its own size.
What is drawn first lies in the back.

## ✦ Build your own module

A module is a small Python class: it gets the display size and returns one image per frame.
`t` is the time in seconds since the module became active – perfect for animations.

**1.** Create `src/ledmatrix/modules/bounce.py`:

```python
"""A dot moving from left to right."""

from PIL import Image, ImageDraw

from ledmatrix.modules.base import Module


class Bounce(Module):
    def __init__(self, width: int, height: int, color=(255, 0, 80), **kwargs) -> None:
        super().__init__(width, height, **kwargs)
        self.color = tuple(color)

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        x = int(t * 40) % self.width
        y = self.height // 2
        ImageDraw.Draw(img).ellipse((x - 3, y - 3, x + 3, y + 3), fill=self.color)
        return img
```

**2.** Register it in `src/ledmatrix/modules/__init__.py`:

```python
from ledmatrix.modules.bounce import Bounce

REGISTRY = {
    "clock": Clock,
    "bounce": Bounce,
}
```

**3.** Add it to your `config/config.yaml`:

```yaml
  - type: bounce
    duration: 8
    color: [255, 0, 80]
```

Check it with `python -m ledmatrix --preview` – done.

> [!TIP]
> Always calculate with `self.width` and `self.height`, never with fixed numbers –
> then your module works on every panel setup.
> Pass `**kwargs` on to `super().__init__()` – that's how your module gets the language.

### Texts in several languages

Put your texts into `texts` and read them with `self.text(...)`:

```python
from PIL import Image, ImageDraw

from ledmatrix.fonts import fit_font
from ledmatrix.modules.base import Module


class Greeting(Module):
    texts = {
        "en": {"hello": "Hello!"},
        "de": {"hello": "Hallo!"},
    }

    def render(self, t: float) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height))
        font = fit_font(self.text("hello"), self.width - 4, self.height - 4)
        ImageDraw.Draw(img).text((self.width / 2, self.height / 2), self.text("hello"),
                                 font=font, fill=(255, 255, 255), anchor="mm")
        return img
```

`fit_font` (from `ledmatrix.fonts`) finds the largest font size that fits – using the bundled
[Inter](https://github.com/rsms/inter) font with full support for umlauts and accents.

---

## ✦ Project structure

```
Waveshare-P2.5-LED-Matrix/
├── config/
│   └── config.example.yaml     template for your config.yaml
├── docs/                       translations, roadmap, images
├── examples/                   example files, e.g. star.gif
├── src/ledmatrix/
│   ├── __main__.py             entry point (python -m ledmatrix)
│   ├── config.py               load and validate the config
│   ├── fonts.py                font helpers (bundled Inter font)
│   ├── renderer.py             output to the LED panels
│   ├── scheduler.py            plays the modules one after another
│   ├── modules/
│   │   ├── base.py             base class for all modules (incl. translations)
│   │   ├── clock.py            clock module
│   │   ├── christmas.py        Christmas countdown
│   │   ├── countdown.py        countdown to any date
│   │   ├── gif.py              GIF player
│   │   └── scrolltext.py       scrolling text
│   ├── widgets/                building blocks for modules
│   │   ├── base.py             base class for all widgets
│   │   ├── effects/            moving effects – snow
│   │   ├── media/              images and animations – GIF
│   │   └── text/               text – scrolling text, countdown
│   ├── preview/
│   │   ├── renderer.py         web server for the browser preview
│   │   └── index.html          preview page
│   └── assets/fonts/           Inter font and its license
└── pyproject.toml              project metadata and dependencies
```

## ✦ Hardware

- **Raspberry Pi 4** (headless, via SSH)
- **4× Waveshare RGB-Matrix P2.5, 64×32** in a 2×2 grid → **128×64 pixels**
- Driven by [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix), GPIO mapping `regular`
- Custom wiring via the GPIO header, two parallel chains of two panels each
- Separate 5 V power supply for the panels (Waveshare: up to 2.5 A per panel)

*Wiring diagram and terminal plan will follow.*

## ✦ Troubleshooting

<details>
<summary><code>snd_bcm2835: found that the Pi sound module is loaded</code></summary>

<br>The on-board sound is still active. Do [step 2](#2--disable-the-on-board-sound) and reboot.
</details>

<details>
<summary><code>make: No rule to make target 'build-python'</code></summary>

<br>The Python bindings of rpi-rgb-led-matrix are built with `pip` since February 2026.
Use `pip install ~/rpi-rgb-led-matrix` inside the activated virtual environment.
</details>

<details>
<summary><code>ModuleNotFoundError: No module named 'ledmatrix'</code> or <code>'rgbmatrix'</code></summary>

<br>The virtual environment is not active – run `source .venv/bin/activate`.
With `sudo`, always use the Python of the venv: `sudo .venv/bin/python -m ledmatrix`.
</details>

<details>
<summary>Image appears twice, flickers or panels stay dark</summary>

<br>Check that `chain_length` and `parallel` match the panels that are really connected.
</details>

<details>
<summary>Wrong colors</summary>

<br>Try another `rgb_sequence` (e.g. `RBG`, `GRB`). A red text must appear red, a green one green.
</details>

<details>
<summary>One chain only shows some rows (stripes)</summary>

<br>An address line (A, B, C or D) is missing on that chain – check the wiring.
</details>

## ✦ Ideas & contributions

This project lives from ideas – **yours are very welcome!**

- 💡 **An idea or a wish?** [Open an issue](https://github.com/gerry-git-ops/Waveshare-P2.5-LED-Matrix/issues/new) and describe it.
- 🧩 **Need a special module?** Describe what it should show – I'm happy to build modules on request.
- 🐞 **Found a bug?** Open an issue with what you did, what you expected and, if possible, a photo of the panels.
- 🔧 **Built something yourself?** A new module, widget or language – pull requests are welcome.

## ✦ License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

It builds on [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) by Henner Zeller (GPL).
The bundled font [Inter](https://github.com/rsms/inter) is licensed under the
[SIL Open Font License 1.1](src/ledmatrix/assets/fonts/OFL.txt).

## ✦ Roadmap

What is planned and what is already running: [ROADMAP](/docs/roadmap.md)

---

<div align="center">
<sub>A project for learning, building and glowing.</sub>
</div>
