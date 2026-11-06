"""Start the web interface next to the display."""

import threading

from ledmatrix.config import Config
from ledmatrix.scheduler import Scheduler
from ledmatrix.web.hub import FrameHub


def start_web(cfg: Config, scheduler: Scheduler, hub: FrameHub,
              port: int, preview: bool) -> bool:
    """Run the web interface in a background thread. False if the web extra is missing."""
    try:
        import uvicorn

        from ledmatrix.web.api import create_app
    except ImportError:
        return False

    app = create_app(cfg, scheduler, hub, preview)
    server = uvicorn.Server(uvicorn.Config(app, host=cfg.web.host, port=port, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    print(f"Web interface on http://localhost:{port}  (stop with Ctrl+C)")
    return True