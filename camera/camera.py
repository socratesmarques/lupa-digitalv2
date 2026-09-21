"""Abertura de webcam com baixa latência e fallback para Linux/Orange Pi."""
from __future__ import annotations

import sys
import time

import cv2


class Camera:
    def __init__(self, device=0, width: int = 640, height: int = 480, fps: int = 24,
                 buffer_size: int = 1, prefer_mjpg: bool = True, index=None):
        if index is not None:
            device = index
        self.device = int(device) if str(device).isdigit() else str(device)
        self.width, self.height, self.fps = width, height, fps
        self.buffer_size, self.prefer_mjpg = buffer_size, prefer_mjpg
        self.cap = None

    def open(self) -> bool:
        self.release()
        backends = [cv2.CAP_V4L2, cv2.CAP_ANY] if sys.platform.startswith("linux") else [cv2.CAP_ANY]
        devices = (0, 2, 1, 3) if self.device == "auto" else (self.device,)
        for device in devices:
            for backend in backends:
                cap = cv2.VideoCapture(device, backend)
                if not cap.isOpened():
                    cap.release()
                    continue
                if self.prefer_mjpg:
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                cap.set(cv2.CAP_PROP_FPS, self.fps)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, self.buffer_size)
                self.cap = cap
                self.active_device = device
                for _ in range(3):
                    cap.grab()
                    time.sleep(0.01)
                return True
        return False

    def is_opened(self) -> bool:
        return self.cap is not None and self.cap.isOpened()

    def read(self):
        return self.cap.read() if self.is_opened() else (False, None)

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def info(self) -> str:
        if not self.is_opened():
            return "Câmera desconectada"
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        return f"Câmera {self.active_device} · {width}×{height} · {fps:.0f} FPS"


CameraVF0780 = Camera
