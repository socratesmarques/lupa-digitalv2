"""Tela principal: captura, processamento e controles da lupa."""
from __future__ import annotations

from datetime import datetime
from time import perf_counter

import cv2
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from camera.camera import Camera
from config.settings import (
    CAMERA_BUFFER_SIZE, CAMERA_DEVICE, CAMERA_FPS, CAMERA_HEIGHT, CAMERA_RETRY_MS,
    CAMERA_WIDTH, DEFAULT_READING_MODE_INDEX, DEFAULT_ZOOM_INDEX, FRAME_INTERVAL_MS,
    PAN_STEP, PREFER_MJPG, SCREENSHOT_DIR, SHOW_READING_GUIDE, ZOOM_LEVELS,
)
from hardware.botoes_gpio import BotoesGPIO
from hardware.controles import Acao
from interface.camera_view import CameraView
from processamento.modos_leitura import MODOS, NOMES
from processamento.pipeline import processar


class PaginaLupa(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.camera = Camera(CAMERA_DEVICE, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS,
                             CAMERA_BUFFER_SIZE, PREFER_MJPG)
        self.timer = QTimer(self); self.timer.timeout.connect(self.atualizar_frame)
        self.gpio_timer = QTimer(self); self.gpio_timer.timeout.connect(self.ler_gpio)
        self.botoes_gpio = BotoesGPIO()
        self.retry_timer = QTimer(self); self.retry_timer.setSingleShot(True)
        self.retry_timer.timeout.connect(self.iniciar_camera)
        self.zoom_index = min(DEFAULT_ZOOM_INDEX, len(ZOOM_LEVELS) - 1)
        self.mode_index = min(DEFAULT_READING_MODE_INDEX, len(MODOS) - 1)
        self.center_x = self.center_y = 0.5
        self.frozen = False
        self.guide = SHOW_READING_GUIDE
        self.enhancement = False
        self.last_raw = self.last_processed = None
        self.frame_count = 0
        self.fps = 0.0
        self.fps_started = perf_counter()
        self._build_ui()

    def _button(self, text, callback, checkable=False, object_name=""):
        button = QPushButton(text); button.setCheckable(checkable)
        if object_name: button.setObjectName(object_name)
        button.clicked.connect(callback)
        return button

    def _build_ui(self):
        root = QHBoxLayout(self); root.setContentsMargins(14, 14, 14, 14); root.setSpacing(14)
        self.view = CameraView(); self.view.set_guide(self.guide); root.addWidget(self.view, 1)
        panel = QFrame(); panel.setObjectName("painel"); panel.setMaximumWidth(300)
        controls = QVBoxLayout(panel); controls.setContentsMargins(16, 16, 16, 16)
        self.zoom_label = QLabel(); self.zoom_label.setObjectName("valorZoom"); self.zoom_label.setAlignment(Qt.AlignCenter)
        self.mode_label = QLabel(); self.mode_label.setObjectName("modo"); self.mode_label.setAlignment(Qt.AlignCenter); self.mode_label.setWordWrap(True)
        controls.addWidget(self.zoom_label); controls.addWidget(self.mode_label)
        zoom_row = QHBoxLayout()
        zoom_row.addWidget(self._button("−", self.zoom_out, object_name="zoom"))
        zoom_row.addWidget(self._button("+", self.zoom_in, object_name="zoom"))
        controls.addLayout(zoom_row)
        move = QGridLayout()
        move.addWidget(self._button("↑", lambda: self.pan(0, -PAN_STEP)), 0, 1)
        move.addWidget(self._button("←", lambda: self.pan(-PAN_STEP, 0)), 1, 0)
        move.addWidget(self._button("Centralizar", self.center), 1, 1)
        move.addWidget(self._button("→", lambda: self.pan(PAN_STEP, 0)), 1, 2)
        move.addWidget(self._button("↓", lambda: self.pan(0, PAN_STEP)), 2, 1)
        controls.addLayout(move)
        self.freeze_button = self._button("Congelar imagem", self.toggle_freeze, True)
        self.guide_button = self._button("Guia de leitura", self.toggle_guide, True); self.guide_button.setChecked(self.guide)
        self.enhance_button = self._button("Melhorar texto", self.toggle_enhancement, True)
        controls.addWidget(self.freeze_button)
        controls.addWidget(self._button("Trocar modo de leitura", self.next_mode))
        controls.addWidget(self.guide_button); controls.addWidget(self.enhance_button)
        controls.addWidget(self._button("Salvar captura", self.save_capture, object_name="primario"))
        controls.addStretch()
        self.status = QLabel("Preparando câmera…"); self.status.setObjectName("rodape"); self.status.setWordWrap(True)
        controls.addWidget(self.status); root.addWidget(panel)
        self._refresh_labels()

    def iniciar_camera(self):
        self.timer.stop(); self.view.set_message(f"Abrindo câmera {CAMERA_DEVICE}…")
        if self.camera.open():
            self.status.setText(self.camera.info()); self.timer.start(FRAME_INTERVAL_MS)
            self.botoes_gpio.iniciar(); self.gpio_timer.start(35)
        else:
            self.view.set_message(f"Não foi possível abrir a câmera {CAMERA_DEVICE}.\nVerifique a conexão ou use LUPA_CAMERA=/dev/video2.")
            self.status.setText("Câmera indisponível · nova tentativa automática")
            self.retry_timer.start(CAMERA_RETRY_MS)

    def parar_camera(self):
        self.timer.stop(); self.gpio_timer.stop(); self.retry_timer.stop()
        self.botoes_gpio.encerrar(); self.camera.release()

    def atualizar_frame(self):
        if self.frozen and self.last_raw is not None:
            raw = self.last_raw
        else:
            ok, raw = self.camera.read()
            if not ok or raw is None:
                self.parar_camera(); self.view.set_message("Sinal da câmera perdido. Reconectando…")
                self.retry_timer.start(CAMERA_RETRY_MS); return
            self.last_raw = raw.copy()
        processed = processar(raw, ZOOM_LEVELS[self.zoom_index], self.center_x,
                              self.center_y, MODOS[self.mode_index], self.enhancement)
        self.last_processed = processed.copy()
        self.frame_count += 1
        elapsed = perf_counter() - self.fps_started
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed; self.frame_count = 0; self.fps_started = perf_counter()
        rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        h, w, channels = rgb.shape
        image = QImage(rgb.data, w, h, channels * w, QImage.Format_RGB888).copy()
        self.view.set_pixmap(QPixmap.fromImage(image), self.fps)

    def zoom_in(self):
        self.zoom_index = min(self.zoom_index + 1, len(ZOOM_LEVELS) - 1); self._refresh_labels()

    def zoom_out(self):
        self.zoom_index = max(self.zoom_index - 1, 0); self._refresh_labels()

    def pan(self, dx, dy):
        self.center_x = max(0.0, min(1.0, self.center_x + dx))
        self.center_y = max(0.0, min(1.0, self.center_y + dy))

    def center(self): self.center_x = self.center_y = 0.5

    def toggle_freeze(self):
        if self.last_raw is None:
            self.freeze_button.setChecked(False); return
        self.frozen = self.freeze_button.isChecked()
        self.freeze_button.setText("Retomar câmera" if self.frozen else "Congelar imagem")

    def next_mode(self):
        self.mode_index = (self.mode_index + 1) % len(MODOS); self._refresh_labels()

    def toggle_guide(self):
        self.guide = self.guide_button.isChecked(); self.view.set_guide(self.guide)

    def toggle_enhancement(self): self.enhancement = self.enhance_button.isChecked()

    def save_capture(self):
        if self.last_processed is None:
            self.status.setText("Ainda não há imagem para salvar."); return
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        path = SCREENSHOT_DIR / datetime.now().strftime("captura_%Y-%m-%d_%H-%M-%S.png")
        self.status.setText(f"Captura salva: {path.name}" if cv2.imwrite(str(path), self.last_processed) else "Falha ao salvar a captura.")

    def _refresh_labels(self):
        self.zoom_label.setText(f"{ZOOM_LEVELS[self.zoom_index]:.2f}×")
        self.mode_label.setText(NOMES[MODOS[self.mode_index]])

    def ler_gpio(self):
        action = self.botoes_gpio.ler()
        actions = {
            Acao.ZOOM_MAIS: self.zoom_in, Acao.ZOOM_MENOS: self.zoom_out,
            Acao.ESQUERDA: lambda: self.pan(-PAN_STEP, 0), Acao.DIREITA: lambda: self.pan(PAN_STEP, 0),
            Acao.CIMA: lambda: self.pan(0, -PAN_STEP), Acao.BAIXO: lambda: self.pan(0, PAN_STEP),
            Acao.CENTRALIZAR: self.center, Acao.PROXIMO_MODO: self.next_mode,
        }
        if action == Acao.FREEZE:
            self.freeze_button.toggle(); self.toggle_freeze()
        elif action in actions: actions[action]()
