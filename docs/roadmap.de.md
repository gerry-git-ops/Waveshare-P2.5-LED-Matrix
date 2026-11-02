[English](/docs/roadmap.md) | **Deutsch**

<div align="center">

# ✦ Roadmap

*Wo das Projekt steht und wohin es geht.*

![Status](https://img.shields.io/badge/Status-im%20Aufbau-orange)

</div>

**Legende:** ✅ erledigt · 🔜 als Nächstes · 💡 Idee

---

## Phase 0 – Fundament

- [x] Raspberry Pi 4 startet von einer USB-Festplatte, ohne Desktop
- [x] Entwicklung per SSH mit Schlüssel-Anmeldung
- [x] Git und GitHub eingerichtet (SSH-Schlüssel, private Commit-Mail)
- [x] Repo-Gerüst: README, Roadmap, `.gitignore`

## Phase 1 – Hardware in Betrieb nehmen 🔜

- [x] [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) installieren und Demo-Programme bauen
- [ ] Python-Anbindung der Bibliothek installieren
- [ ] Demo-Programme auf den Panels laufen lassen
- [ ] Panel-Reihenfolge prüfen (zwei parallele Ketten mit je zwei Panels)
- [ ] Farbreihenfolge korrigieren (diese Panels brauchen `RBG`)
- [ ] `gpio_slowdown` und Helligkeit für ein flackerfreies Bild einstellen

## Phase 2 – Kern

- [ ] Renderer, der pro Frame ein Bild mit 128×64 Pixeln erzeugt
- [ ] Modul-Schnittstelle (`render(t)`) und Modul-Lader
- [ ] Scheduler: Reihenfolge und Dauer der Module
- [ ] Konfiguration über `config.yaml` (mit Vorlage `config.example.yaml`)
- [ ] Hardware-unabhängiger Aufbau: Panelgröße, Reihen, Kettenlänge und Verdrahtung nur in der `config.yaml`
- [ ] Vorschau-Modus ohne Hardware, um Module am PC zu entwickeln

## Phase 3 – Erste Module

- [ ] Lauftext
- [ ] Uhr
- [ ] Countdown
- [ ] GIF-Player

## Phase 4 – Dauerbetrieb

- [ ] Autostart als systemd-Dienst
- [ ] Helligkeitsplan (nachts dunkler)
- [ ] Sauberes Beenden und Neustart bei Fehlern

## Phase 5 – Ideen 💡

- [ ] Krypto-Ticker mit Kursverlauf
- [ ] Wetter-Modul
- [ ] Steuerung und Einstellungen über eine Webseite
- [ ] Übergänge zwischen den Modulen
- [ ] API-Schnittstelle (Matrix an/aus) für Befehle von externen Geräten (z.B. Siemens S7)

---

Zurück zur [README](/docs/README.de.md).