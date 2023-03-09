from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPainter, QTransform, QVector2D, QMouseEvent
#from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt 
import numpy as np
from .engine import DummyWorld, World, Car

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 800)
        print("Hello MainWindow")
        self.world = DummyWorld()
        self.camera = Camera()

        self.pan_last_pos = None

    def paintEvent(self, event) -> None:
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            self.camera.draw(painter, self.world)

        return super().paintEvent(event)
    
    def wheelEvent(self, event) -> None:
        angle = event.angleDelta().y() / 8
        factor = np.power(1.01, angle)
        self.camera.scale *= factor
        self.update()
        return super().wheelEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.pan_last_pos = QVector2D(event.pos())
            print(f"pressed at {self.pan_last_pos}")

        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            print("released")
            self.pan_last_pos = None
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.pan_last_pos:
            pos = QVector2D(event.pos())
            v = pos - self.pan_last_pos
            v.setY(-v.y())
            self.camera.center -= v/self.camera.scale
            self.update()
            self.pan_last_pos = pos

        return super().mouseMoveEvent(event)
    
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
            global_transform = self.get_transform(car)
            painter.setTransform(global_transform * transform)
            
            self.draw_car(car, painter)

    def draw_car(self, car: Car, painter: QPainter):
        painter.fillRect(-20, -10, 40, 20, "Grey")

        color = "Blue"
        if "special" in car.get_tags():
            color = "Red"      
        painter.fillRect(10, -6, 5, 12, color)

        painter.drawPoint(0, 0)
    
    def get_transform(self, car: Car) -> QTransform:
        position = car.get_position()
        heading = car.get_heading()

        t = QTransform()
        t.translate(*position)
        r = np.arctan2(*heading[::-1])
        t.rotateRadians(r)

        return t