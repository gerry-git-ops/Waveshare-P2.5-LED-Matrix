"""Browser preview: shows the frames as LEDs, no hardware needed."""

import base64
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources

from PIL import Image

from ledmatrix.config import HardwareConfig


class PreviewRenderer:
    """Same interface as MatrixRenderer, but streams frames to a web page."""

    def __init__(self, hw: HardwareConfig, port: int = 8080) -> None:
        self.width = hw.width
        self.height = hw.height
        self._frame = b""
        self._frame_id = 0
        self._new_frame = threading.Condition()

        self._server = ThreadingHTTPServer(("0.0.0.0", port), self._make_handler())
        self._server.daemon_threads = True
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        print(f"Preview running on http://localhost:{port}  (stop with Ctrl+C)")

    def show(self, image: Image.Image) -> None:
        """Hand one frame to all connected browsers."""
        data = base64.b64encode(image.convert("RGB").tobytes())
        with self._new_frame:
            self._frame = data
            self._frame_id += 1
            self._new_frame.notify_all()

    def clear(self) -> None:
        """Send a black frame."""
        self.show(Image.new("RGB", (self.width, self.height)))

    def _wait_for_frame(self, last_id: int) -> tuple[int, bytes]:
        """Block until there is a frame newer than last_id."""
        with self._new_frame:
            self._new_frame.wait_for(lambda: self._frame_id != last_id)
            return self._frame_id, self._frame

    def _make_handler(self) -> type[BaseHTTPRequestHandler]:
        renderer = self
        page = resources.files("ledmatrix.preview").joinpath("index.html").read_bytes()
        size = f"{self.width}x{self.height}:".encode()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                if self.path == "/":
                    self._send(page, "text/html; charset=utf-8")
                elif self.path == "/stream":
                    self._stream()
                else:
                    self.send_error(404)

            def _send(self, body: bytes, content_type: str) -> None:
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def _stream(self) -> None:
                # Server-Sent Events: one long-lived response, one message per frame
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                last_id = -1
                try:
                    while True:
                        last_id, frame = renderer._wait_for_frame(last_id)
                        self.wfile.write(b"data: " + size + frame + b"\n\n")
                        self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass  # browser tab was closed

            def log_message(self, *args) -> None:
                pass  # keep the console quiet

        return Handler