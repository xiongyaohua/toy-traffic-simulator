from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPainter, QTransform, QVector2D
#from PySide6.QtCore import QPointF
import numpy as np
from .engine import DummyWorld, World

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 800)
        print("Hello MainWindow")
        self.world = DummyWorld()
        self.camera = Camera()

    def paintEvent(self, event) -> None:
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            self.camera.paint(painter, self.width(), self.height(), self.world)

        return super().paintEvent(event)
    
class Camera:
    def __init__(self) -> None:
        self.center = QVector2D(300, 300)
        self.scale = QVector2D(0.5, 0.5)

    def paint(self, painter: QPainter, width: int, height: int, world: World):
        vt = self.get_transform(width, height)
        painter.setTransform(vt)
        painter.drawPoint(300,300)
        for car in world.get_cars():
            t = car.get_transform()
            painter.setTransform(t * vt)
            
            self.draw_car(car, painter)

    def draw_car(self, car, painter: QPainter):
        painter.drawRect(-20, -10, 40, 20)
        painter.fillRect(10, -6, 5, 12, "Blue")

    def get_transform(self, width, height) -> QTransform:
        t = QTransform()
        t.translate(-self.center.x()+width/2, self.center.y()+height/2)
        t.scale(self.scale.x(), -self.scale.y())
        return t
