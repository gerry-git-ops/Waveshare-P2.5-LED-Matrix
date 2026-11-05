"""Entry point: python -m ledmatrix [config file]"""

import sys

from ledmatrix.config import load_config
from ledmatrix.modules import create_module
from ledmatrix.renderer import MatrixRenderer
from ledmatrix.scheduler import Scheduler


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "config/config.yaml"
    cfg = load_config(path)

    hw = cfg.hardware
    modules = [create_module(m, hw.width, hw.height) for m in cfg.modules]

    renderer = MatrixRenderer(hw)
    try:
        Scheduler(renderer, modules, fps=cfg.fps).run()
    except KeyboardInterrupt:
        renderer.clear()


if __name__ == "__main__":
    main()