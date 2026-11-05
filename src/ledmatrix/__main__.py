"""Entry point: python -m ledmatrix [config file] [--preview]"""

import argparse

from ledmatrix.config import load_config
from ledmatrix.modules import create_module
from ledmatrix.scheduler import Scheduler


def main() -> None:
    parser = argparse.ArgumentParser(prog="ledmatrix")
    parser.add_argument("config", nargs="?", default="config/config.yaml",
                        help="path to the config file")
    parser.add_argument("--preview", action="store_true",
                        help="show the output in a browser instead of the panels")
    parser.add_argument("--port", type=int, default=8080,
                        help="port for the preview (default: 8080)")
    args = parser.parse_args()

    cfg = load_config(args.config)
    hw = cfg.hardware
    modules = [create_module(m, hw.width, hw.height, cfg.language) for m in cfg.modules]

    if args.preview:
        from ledmatrix.preview.renderer import PreviewRenderer
        renderer = PreviewRenderer(hw, port=args.port)
    else:
        from ledmatrix.renderer import MatrixRenderer
        renderer = MatrixRenderer(hw)

    try:
        Scheduler(renderer, modules, fps=cfg.fps).run()
    except KeyboardInterrupt:
        renderer.clear()


if __name__ == "__main__":
    main()