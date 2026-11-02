**English** | [Deutsch](roadmap.de.md)

<div align="center">

# ✦ Roadmap

*Where the project stands and where it is going.*

![Status](https://img.shields.io/badge/Status-work%20in%20progress-orange)

</div>

**Legend:** ✅ done · 🔜 next · 💡 idea

---

## Phase 0 – Foundation

- [x] Raspberry Pi 4 boots from a USB drive, headless (no desktop)
- [x] Remote development over SSH with key authentication
- [x] Git and GitHub set up (SSH key, private commit e-mail)
- [x] Repository scaffold: README, roadmap, `.gitignore`

## Phase 1 – Hardware bring-up 🔜

- [x] Install [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) and build the demo programs
- [ ] Install the Python bindings of the library
- [ ] Run the demo programs on the panels
- [ ] Verify panel order (two parallel chains of two panels)
- [ ] Fix the color order (these panels need `RBG`)
- [ ] Tune `gpio_slowdown` and brightness for a flicker-free image

## Phase 2 – Core

- [ ] Renderer that produces one 128×64 image per frame
- [ ] Module interface (`render(t)`) and module loader
- [ ] Scheduler: order and duration of modules
- [ ] Configuration via `config.yaml` (plus a `config.example.yaml` template)
- [ ] Hardware-independent design: panel size, rows, chain length and wiring only in `config.yaml`
- [ ] Preview mode without hardware, for developing modules on a PC

## Phase 3 – First modules

- [ ] Scrolling text
- [ ] Clock
- [ ] Countdown
- [ ] GIF player

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