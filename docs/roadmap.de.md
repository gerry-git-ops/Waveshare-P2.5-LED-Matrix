[English](/docs/roadmap.md) | **Deutsch**

<div align="center">

# ✦ Roadmap

*Wo das Projekt steht und wohin es geht.*

![Status](https://img.shields.io/badge/Status-im%20Aufbau-orange)

</div>

**Legende:** ✅ erledigt · 🔜 als Nächstes · 💡 Idee

---

## Phase 0 – Fundament ✅

- [x] Raspberry Pi 4 startet von einer USB-Festplatte, ohne Desktop
- [x] Entwicklung per SSH mit Schlüssel-Anmeldung
- [x] Git und GitHub eingerichtet (SSH-Schlüssel, private Commit-Mail)
- [x] Repo-Gerüst: README, Roadmap, `.gitignore`

## Phase 1 – Hardware in Betrieb nehmen ✅

- [x] [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) installieren und Demo-Programme bauen
- [x] Python-Anbindung der Bibliothek installieren
- [x] Demo-Programme auf den Panels laufen lassen
- [x] Panel-Reihenfolge prüfen (zwei parallele Ketten mit je zwei Panels)
- [x] Farbreihenfolge korrigieren (diese Panels brauchen `RBG`)
- [x] `gpio_slowdown` und Helligkeit für ein flackerfreies Bild einstellen

## Phase 2 – Kern ✅

- [x] Renderer, der pro Frame ein Bild mit 128×64 Pixeln erzeugt
- [x] Modul-Schnittstelle (`render(t)`) und Modul-Lader
- [x] Scheduler: Reihenfolge und Dauer der Module
- [x] Konfiguration über `config.yaml` (mit Vorlage `config.example.yaml`)
- [x] Hardware-unabhängiger Aufbau: Panelgröße, Reihen, Kettenlänge und Verdrahtung nur in der `config.yaml`
- [x] Vorschau-Modus ohne Hardware, um Module am PC zu entwickeln

## Phase 3 – Erste Module ✅

- [x] Lauftext (einfarbig oder Regenbogen, mit festgelegter Anzahl Durchläufe)
- [x] Module in der Config ein- und ausschalten (`enabled`)
- [x] Uhr
- [x] Weihnachts-Countdown mit Lichterkette, Baum und Schnee 🎄
- [x] Texte in mehreren Sprachen (en, de, fr, es)
- [x] Countdown zu einem beliebigen Datum
- [x] GIF-Player mit Beispiel-GIF
- [x] Widgets als wiederverwendbare Bausteine, in Ordnern sortiert (Text, Medien, Effekte, Kulisse)
- [x] Reise-Countdown: Schiff, Meer, Himmel und Teilchen-Effekte 🚢
- [x] Farbpaletten für alle Texte
- [x] Finale für das Reise-Modul: eigene Clips und Bilder mit Übergängen

## Phase 4 – Dauerbetrieb 🔜

- [ ] Autostart als systemd-Dienst
- [ ] Helligkeitsplan (nachts dunkler)
- [ ] Helligkeits-Zuschlag pro Modul oder Finale-Teil, auf die aktuelle Helligkeit drauf (z. B. +25 % für Videos)
- [ ] Sauberes Beenden und Neustart bei Fehlern

## Phase 5 – Ideen 💡

- [ ] Krypto-Ticker mit Kursverlauf
- [ ] Wetter-Modul
- [x] Web-Oberfläche: Live-Bild, laufendes Modul, Module und Hardware, Hell/Dunkel
- [ ] Einstellungen über die Webseite ändern (Module an/aus, Helligkeit, Optionen, Uploads)
- [ ] Übergänge zwischen den Modulen (das Überblenden selbst ist in `transitions.py` schon fertig)
- [ ] API-Schnittstelle (Matrix an/aus) für Befehle von externen Geräten (z.B. Siemens S7)

> 💡 **Dir fehlt etwas?** [Eröffne ein Issue](https://github.com/gerry-git-ops/Waveshare-P2.5-LED-Matrix/issues/new) – Ideen und Modulwünsche sind willkommen.

---

Zurück zur [README](/docs/README.de.md).