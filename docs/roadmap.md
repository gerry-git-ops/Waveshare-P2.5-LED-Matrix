**English** | [Deutsch](roadmap.de.md)

<div align="center">

# ✦ Roadmap

*Where the project stands and where it is going.*

![Status](https://img.shields.io/badge/Status-work%20in%20progress-orange)

</div>

**Legend:** ✅ done · 🔜 next · 💡 idea

---

## Phase 0 – Foundation ✅

- [x] Raspberry Pi 4 boots from a USB drive, headless (no desktop)
- [x] Remote development over SSH with key authentication
- [x] Git and GitHub set up (SSH key, private commit e-mail)
- [x] Repository scaffold: README, roadmap, `.gitignore`

## Phase 1 – Hardware bring-up ✅

- [x] Install [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) and build the demo programs
- [x] Install the Python bindings of the library
- [x] Run the demo programs on the panels
- [x] Verify panel order (two parallel chains of two panels)
- [x] Fix the color order (these panels need `RBG`)
- [x] Tune `gpio_slowdown` and brightness for a flicker-free image

## Phase 2 – Core ✅

- [x] Renderer that produces one 128×64 image per frame
- [x] Module interface (`render(t)`) and module loader
- [x] Scheduler: order and duration of modules
- [x] Configuration via `config.yaml` (plus a `config.example.yaml` template)
- [x] Hardware-independent design: panel size, rows, chain length and wiring only in `config.yaml`
- [x] Preview mode without hardware, for developing modules on a PC

## Phase 3 – First modules 🔜

- [x] Scrolling text (color or rainbow, runs a set number of loops)
- [x] Switch modules on and off in the config (`enabled`)
- [x] Clock
- [x] Christmas countdown with garland, tree and snow 🎄
- [x] Texts in several languages (en, de, fr, es)
- [ ] Countdown to any date
- [x] GIF player with example GIF
- [x] Widgets as reusable building blocks (scrolling text, GIF, snow)

## Phase 4 – Running it for real

- [ ] Autostart as a systemd service
- [ ] Brightness schedule (dimmer at night)
- [ ] Clean shutdown and restart on errors

## Phase 5 – Ideas 💡

- [ ] Crypto ticker with price history
- [ ] Weather module
- [ ] Control and configuration from a web page
- [ ] Transitions between modules
- [ ] API interface (matrix on/off) for commands from external devices (e.g. Siemens S7)

---

Back to the [README](../README.md).