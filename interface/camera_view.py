"""Widget que desenha a imagem mantendo proporção, sem cv2.imshow()."""
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPixmap
from PySide6.QtWidgets import QSizePolicy, QWidget


class CameraView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._image = QPixmap()
        self._message = "Iniciando câmera…"
        self._fps = 0.0
        self._guide = False
        self.setMinimumSize(320, 240)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def set_pixmap(self, pixmap: QPixmap, fps: float = 0.0):
        self._image, self._message, self._fps = pixmap, "", fps
        self.update()

    def set_message(self, message: str):
        self._image, self._message = QPixmap(), message
        self.update()

    def set_guide(self, enabled: bool):
        self._guide = enabled
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#050a10"))
        if self._image.isNull():
            painter.setPen(QColor("#a9bfd5"))
            font = painter.font(); font.setPixelSize(18); painter.setFont(font)
            painter.drawText(self.rect().adjusted(30, 20, -30, -20),
                             Qt.AlignCenter | Qt.TextWordWrap, self._message)
            return
        size = self._image.size().scaled(self.size(), Qt.KeepAspectRatio)
        left = (self.width() - size.width()) // 2
        top = (self.height() - size.height()) // 2
        painter.drawPixmap(left, top, size.width(), size.height(), self._image)
        painter.fillRect(QRectF(14, 14, 190, 27), QColor(11, 17, 24, 210))
        painter.setPen(QColor("#d7e7f7"))
        font = painter.font(); font.setPixelSize(11); painter.setFont(font)
        painter.drawText(QRectF(24, 14, 175, 27), Qt.AlignVCenter,
                         f"CÂMERA AO VIVO · {self._fps:.0f} FPS")
        if self._guide:
            center = top + size.height() * 0.53
            band = min(88, size.height() * 0.16)
            painter.fillRect(QRectF(left, top, size.width(), center - band / 2 - top), QColor(0, 0, 0, 125))
            painter.fillRect(QRectF(left, center + band / 2, size.width(), top + size.height() - center - band / 2), QColor(0, 0, 0, 125))
            painter.setPen(QColor(255, 255, 255, 190))
            painter.drawLine(left, int(center - band / 2), left + size.width(), int(center - band / 2))
            painter.drawLine(left, int(center + band / 2), left + size.width(), int(center + band / 2))
