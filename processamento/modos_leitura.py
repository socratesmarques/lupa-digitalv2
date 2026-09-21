import cv2
import numpy as np

MODOS = ["cor_melhorada", "cinza", "alto_contraste", "texto_pb", "texto_invertido", "amarelo_preto"]
NOMES = {
    "cor_melhorada": "Cor melhorada", "cinza": "Escala de cinza",
    "alto_contraste": "Alto contraste", "texto_pb": "Preto no branco",
    "texto_invertido": "Branco no preto", "amarelo_preto": "Amarelo no preto",
}


def _gray(frame): return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def _texto_binario(frame):
    gray = cv2.createCLAHE(clipLimit=2.2, tileGridSize=(8, 8)).apply(_gray(frame))
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 35, 8)


def aplicar_modo(frame, modo):
    if frame is None: return None
    if modo == "cinza": return cv2.cvtColor(_gray(frame), cv2.COLOR_GRAY2BGR)
    if modo == "alto_contraste":
        out = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(_gray(frame))
        return cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
    if modo == "texto_pb": return cv2.cvtColor(_texto_binario(frame), cv2.COLOR_GRAY2BGR)
    if modo == "texto_invertido":
        return cv2.cvtColor(cv2.bitwise_not(_texto_binario(frame)), cv2.COLOR_GRAY2BGR)
    if modo == "amarelo_preto":
        mask = cv2.bitwise_not(_texto_binario(frame))
        out = np.zeros((*mask.shape, 3), dtype=np.uint8); out[mask > 0] = (0, 255, 255)
        return out
    return frame.copy()
