"""The web app: JSON API, live stream and the dashboard page."""

import asyncio
import base64
from importlib import resources

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from ledmatrix.config import Config
from ledmatrix.scheduler import Scheduler
from ledmatrix.web.hub import FrameHub
from ledmatrix.web.host import host_info


def create_app(cfg: Config, scheduler: Scheduler, hub: FrameHub, preview: bool) -> FastAPI:
    """Build the web app for the running display."""
    app = FastAPI(title="LED Matrix", docs_url="/api/docs", redoc_url=None)
    static = resources.files("ledmatrix.web") / "static"
    app.mount("/static", StaticFiles(directory=str(static)), name="static")

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return (static / "index.html").read_text(encoding="utf-8")

    @app.get("/api/status")
    def status() -> dict:
        """What is on screen right now."""
        return {**scheduler.status(), "preview": preview}

    @app.get("/api/config")
    def config() -> dict:
        """Hardware and general settings."""
        hw = cfg.hardware
        return {
            "hardware": {**hw.model_dump(), "width": hw.width, "height": hw.height},
            "fps": cfg.fps,
            "language": cfg.language,
        }

    @app.get("/api/modules")
    def modules() -> list[dict]:
        """All modules from config.yaml, also the switched off ones."""
        return [
            {
                "index": i,
                "type": m.type,
                "enabled": m.enabled,
                "duration": m.duration,
                "options": m.model_extra or {},
            }
            for i, m in enumerate(cfg.modules)
        ]

    @app.get("/api/host")
    def host() -> dict:
        """The computer the matrix runs on: model, CPU, temperature, memory, disk, uptime."""
        return host_info()
        
    @app.get("/api/stream")
    async def stream() -> StreamingResponse:
        """Live picture as Server-Sent Events: one message per new frame."""
        size = f"{hub.width}x{hub.height}:"

        async def events():
            last = -1
            while True:
                frame_id, frame = hub.latest()
                if frame_id != last:
                    last = frame_id
                    yield f"data: {size}{base64.b64encode(frame).decode()}\n\n"
                await asyncio.sleep(1 / cfg.fps)

        return StreamingResponse(events(), media_type="text/event-stream",
                                 headers={"Cache-Control": "no-cache"})

    return app