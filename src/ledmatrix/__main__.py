"""Entry point: python -m ledmatrix [config file] [--preview]"""

import argparse
import sys

from ledmatrix.config import load_config
from ledmatrix.modules import create_module
from ledmatrix.scheduler import Scheduler
from ledmatrix.web.hub import FrameHub
from ledmatrix.web.server import start_web


def main() -> None:
    parser = argparse.ArgumentParser(prog="ledmatrix")
    parser.add_argument("config", nargs="?", default="config/config.yaml",
                        help="path to the config file")
    parser.add_argument("--preview", action="store_true",
                        help="no panels: everything runs, the picture is shown in the browser")
    parser.add_argument("--port", type=int, default=None,
                        help="port for the web interface (default: from the config, 8080)")
    args = parser.parse_args()

    cfg = load_config(args.config)
    hw = cfg.hardware
    modules = [create_module(m, hw.width, hw.height, cfg.language, index=i)
               for i, m in enumerate(cfg.modules) if m.enabled]

    if args.preview:
        panels = None                    # simulate: no hardware needed
    else:
        from ledmatrix.renderer import MatrixRenderer
        panels = MatrixRenderer(hw)

    hub = FrameHub(hw.width, hw.height, target=panels)
    scheduler = Scheduler(hub, modules, fps=cfg.fps)

    if args.preview or cfg.web.enabled:
        port = args.port or cfg.web.port
        if not start_web(cfg, scheduler, hub, port, preview=args.preview):
            hint = 'The web interface needs the web extra:  pip install -e ".[web]"'
            if args.preview:
                sys.exit(hint)           # the preview is nothing without the browser
            print(hint + "  – running without it")

    try:
        scheduler.run()
    except KeyboardInterrupt:
        hub.clear()


def preview() -> None:
    """Shortcut command 'ledmatrix-preview': same as python -m ledmatrix --preview."""
    sys.argv.insert(1, "--preview")
    main()


if __name__ == "__main__":
    main()