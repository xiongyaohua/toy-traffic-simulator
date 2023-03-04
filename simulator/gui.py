from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPainter
from PySide6.QtCore import QPointF

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 800)
        print("Hello MainWindow")

    def paintEvent(self, event) -> None:
        with QPainter(self) as painter:
            painter.drawLine(QPointF(10, 10), QPointF(500, 300))

        return super().paintEvent(event)