from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPainter, QTransform, QVector2D
#from PySide6.QtCore import QPointF
import numpy as np
from .engine import DummyWorld, World, Car

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

            self.camera.draw(painter, self.world)

        return super().paintEvent(event)
    
class Camera:
    def __init__(self) -> None:
        self.center = QVector2D(400, 200)
        self.scale = 0.5

    def draw(self, painter: QPainter, world: World):
        viewport = painter.viewport()
        width = viewport.width()
        height = viewport.height()

        vp_transform = QTransform()
        vp_transform.translate(width/2, height/2)
        vp_transform.scale(1, -1)

        camera_transform = QTransform()
        camera_transform.scale(self.scale, self.scale)
        camera_transform.translate(-self.center.x(), -self.center.y())

        transform = camera_transform * vp_transform

        for car in world.get_cars():
            global_transform = car.get_transform()
            painter.setTransform(global_transform * transform)
            
            self.draw_car(car, painter)

    def draw_car(self, car: Car, painter: QPainter):
        painter.drawRect(-20, -10, 40, 20)

        color = "Blue"
        if "special" in car.get_tags():
            color = "Red"      
        painter.fillRect(10, -6, 5, 12, color)

        painter.drawPoint(0, 0)
