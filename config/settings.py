"""Configuração central com padrões leves para o Orange Pi 3 LTS."""
from __future__ import annotations

import os
import platform
from pathlib import Path

APP_NAME = "Lupa Digital"
VERSION = "2.0.0"
BASE_DIR = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = BASE_DIR / "capturas"

IS_ARM = platform.machine().lower() in {"aarch64", "arm64", "armv7l"}
CAMERA_DEVICE = os.getenv("LUPA_CAMERA", "auto")
CAMERA_WIDTH = int(os.getenv("LUPA_WIDTH", "640" if IS_ARM else "1280"))
CAMERA_HEIGHT = int(os.getenv("LUPA_HEIGHT", "480" if IS_ARM else "720"))
CAMERA_FPS = int(os.getenv("LUPA_FPS", "24" if IS_ARM else "30"))
CAMERA_BUFFER_SIZE = 1
PREFER_MJPG = True
CAMERA_RETRY_MS = 1500
FRAME_INTERVAL_MS = max(20, round(1000 / CAMERA_FPS))
OPENCV_THREADS = 2 if IS_ARM else 4

ZOOM_LEVELS = (1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0)
DEFAULT_ZOOM_INDEX = 2
PAN_STEP = 0.07
UPSCALE_INTERPOLATION = "linear" if IS_ARM else "cubic"
DEFAULT_READING_MODE_INDEX = 0
START_FULLSCREEN = os.getenv("LUPA_FULLSCREEN", "1" if IS_ARM else "0") == "1"
SHOW_READING_GUIDE = False
