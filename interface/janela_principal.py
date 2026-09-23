"""Janela responsiva no mesmo estilo visual do projeto de detecção facial."""
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

from config.settings import PAN_STEP
from interface.pagina_lupa import PaginaLupa
from interface.tema import TEMA


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lupa Digital V2 — Orange Pi")
        self.resize(1024, 768); self.setMinimumSize(720, 480); self.setStyleSheet(TEMA)
        central = QWidget(); layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(0); self.setCentralWidget(central)
        header = QFrame(); header.setObjectName("cabecalho")
        row = QHBoxLayout(header); row.setContentsMargins(18, 8, 18, 8)
        brand = QLabel("Lupa Digital"); brand.setObjectName("marca")
        subtitle = QLabel("V2.0  /  LEITURA ASSISTIDA"); subtitle.setObjectName("subtitulo")
        fullscreen = QPushButton("Tela cheia"); fullscreen.clicked.connect(self.toggle_fullscreen)
        row.addWidget(brand); row.addWidget(subtitle); row.addStretch(); row.addWidget(fullscreen)
        layout.addWidget(header)
        self.page = PaginaLupa(); layout.addWidget(self.page, 1)
        self._shortcut("F11", self.toggle_fullscreen)
        self._shortcut("Escape", self.leave_fullscreen)
        self._shortcut("+", self.page.zoom_in)
        self._shortcut("-", self.page.zoom_out)
        self._shortcut("Left", lambda: self.page.pan(-PAN_STEP, 0))
        self._shortcut("Right", lambda: self.page.pan(PAN_STEP, 0))
        self._shortcut("Up", lambda: self.page.pan(0, -PAN_STEP))
        self._shortcut("Down", lambda: self.page.pan(0, PAN_STEP))
        self._shortcut("Space", self._keyboard_freeze)
        self._shortcut("F", self.page.next_mode)
        self._shortcut("S", self.page.save_capture)
        self._shortcut("C", self.page.center)
        self.page.iniciar_camera()

    def _shortcut(self, key, callback):
        shortcut = QShortcut(QKeySequence(key), self)
        shortcut.activated.connect(callback)

    def _keyboard_freeze(self): self.page.freeze_button.toggle(); self.page.toggle_freeze()
    def toggle_fullscreen(self): self.showNormal() if self.isFullScreen() else self.showFullScreen()
    def leave_fullscreen(self):
        if self.isFullScreen(): self.showNormal()
    def closeEvent(self, event): self.page.parar_camera(); event.accept()
