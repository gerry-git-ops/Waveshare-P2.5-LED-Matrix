"""Information about the computer the matrix runs on (Raspberry Pi or PC)."""

import platform
import socket
import time
from pathlib import Path

import psutil


def _model() -> str:
    """'Raspberry Pi 4 Model B Rev 1.4' on a Pi, otherwise system and processor type."""
    path = Path("/proc/device-tree/model")          # only exists on a Raspberry Pi
    if path.exists():
        return path.read_text(errors="ignore").strip("\x00 \n")
    return f"{platform.system()} · {platform.machine()}"


def _os_name() -> str:
    """Name of the operating system, e.g. 'Debian GNU/Linux 13 (trixie)' or 'Windows-11'."""
    release = Path("/etc/os-release")
    if release.exists():
        for line in release.read_text().splitlines():
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip('"')
    return platform.platform(terse=True)


def _ip() -> str:
    """IP address in the home network (no data is sent, the socket only picks the route)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 80))
            return s.getsockname()[0]
    except OSError:
        return "–"


def _temperature() -> float | None:
    """CPU temperature in °C, None if the system does not report it (e.g. on Windows)."""
    sensors = getattr(psutil, "sensors_temperatures", lambda: {})()
    for name in ("cpu_thermal", "coretemp", "k10temp"):
        if sensors.get(name):
            return round(sensors[name][0].current, 1)
    for entries in sensors.values():
        if entries:
            return round(entries[0].current, 1)
    return None


# things that do not change while the program runs
MODEL = _model()
OS_NAME = _os_name()
psutil.cpu_percent()        # the first call only starts the measurement


def host_info() -> dict:
    """Everything for the host part of the web interface."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(Path.cwd().anchor)     # "/" on Linux, "C:\" on Windows
    freq = psutil.cpu_freq()
    return {
        "model": MODEL,
        "hostname": socket.gethostname(),
        "ip": _ip(),
        "os": OS_NAME,
        "python": platform.python_version(),
        "cpu": {
            "percent": psutil.cpu_percent(),
            "cores": psutil.cpu_count(),
            "mhz": round(freq.current) if freq else None,
            "load": [round(x, 2) for x in psutil.getloadavg()],
        },
        "temperature": _temperature(),
        "memory": {"used": memory.used, "total": memory.total, "percent": memory.percent},
        "disk": {"used": disk.used, "total": disk.total, "percent": disk.percent},
        "uptime": int(time.time() - psutil.boot_time()),
    }