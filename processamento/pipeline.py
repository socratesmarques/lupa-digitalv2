"""Pipeline de imagem independente da interface gráfica."""
from __future__ import annotations

import cv2

from config.settings import UPSCALE_INTERPOLATION
from processamento.modos_leitura import aplicar_modo


def aplicar_zoom(frame, zoom: float, centro_x: float, centro_y: float):
    if frame is None or zoom <= 1.0:
        return None if frame is None else frame.copy()
    h, w = frame.shape[:2]
    roi_w, roi_h = max(4, int(w / zoom)), max(4, int(h / zoom))
    x = int((w - roi_w) * max(0.0, min(1.0, centro_x)))
    y = int((h - roi_h) * max(0.0, min(1.0, centro_y)))
    roi = frame[y:y + roi_h, x:x + roi_w]
    interpolation = cv2.INTER_LINEAR if UPSCALE_INTERPOLATION == "linear" else cv2.INTER_CUBIC
    return cv2.resize(roi, (w, h), interpolation=interpolation)


def melhorar_leitura(frame):
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    light, a, b = cv2.split(lab)
    light = cv2.createCLAHE(clipLimit=1.8, tileGridSize=(8, 8)).apply(light)
    color = cv2.cvtColor(cv2.merge((light, a, b)), cv2.COLOR_LAB2BGR)
    blur = cv2.GaussianBlur(color, (0, 0), 0.9)
    return cv2.addWeighted(color, 1.45, blur, -0.45, 0)


def processar(frame, zoom: float, centro_x: float, centro_y: float,
              modo: str, melhoria_ativa: bool):
    output = aplicar_zoom(frame, zoom, centro_x, centro_y)
    if melhoria_ativa and modo == "cor_melhorada":
        output = melhorar_leitura(output)
    return aplicar_modo(output, modo)
