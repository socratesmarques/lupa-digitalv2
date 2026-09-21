"""Ponto de entrada da Lupa Digital V2 para Orange Pi e desktop."""
from __future__ import annotations

import os
import sys

os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")

import cv2
from PySide6.QtWidgets import QApplication

from config.settings import APP_NAME, OPENCV_THREADS, START_FULLSCREEN, VERSION
from interface.janela_principal import JanelaPrincipal


def main() -> int:
    cv2.setNumThreads(OPENCV_THREADS)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    janela = JanelaPrincipal()
    janela.showFullScreen() if START_FULLSCREEN else janela.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
