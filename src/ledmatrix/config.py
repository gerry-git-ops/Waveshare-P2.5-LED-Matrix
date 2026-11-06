"""Load and validate the configuration file."""

from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field
from pydantic import BaseModel, ConfigDict, Field


class HardwareConfig(BaseModel):
    """Panel and wiring settings, passed on to rpi-rgb-led-matrix."""

    rows: int = Field(32, gt=0)
    cols: int = Field(32, gt=0)
    chain_length: int = Field(1, ge=1)
    parallel: int = Field(1, ge=1, le=3)
    hardware_mapping: str = "regular"
    gpio_slowdown: int = Field(1, ge=0)
    rgb_sequence: Literal["RGB", "RBG", "GRB", "GBR", "BRG", "BGR"] = "RGB"
    brightness: int = Field(100, ge=0, le=100)

    @property
    def width(self) -> int:
        """Total width in pixels."""
        return self.cols * self.chain_length

    @property
    def height(self) -> int:
        """Total height in pixels."""
        return self.rows * self.parallel

class ModuleConfig(BaseModel):
    """One entry in the module list. Extra keys are passed to the module."""

    model_config = ConfigDict(extra="allow")

    type: str
    enabled: bool = True
    duration: float | None = Field(None, gt=0)

class WebConfig(BaseModel):
    """Web interface (needs the web extra: pip install -e ".[web]")."""

    enabled: bool = True
    host: str = "0.0.0.0"      # 0.0.0.0 = reachable in your home network
    port: int = Field(8080, ge=1, le=65535)

class Config(BaseModel):
    """The whole configuration."""

    hardware: HardwareConfig = HardwareConfig()
    web: WebConfig = WebConfig()
    fps: int = Field(30, ge=1, le=120)
    modules: list[ModuleConfig] = []
    language: str = "en"


def load_config(path: Path | str = "config/config.yaml") -> Config:
    """Read a YAML file and return a validated Config."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Config.model_validate(data)