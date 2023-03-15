from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPainter, QTransform, QVector2D, QMouseEvent
#from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt, QTimer
import numpy as np
from .engine import DummyWorld, World, Car
from .road import Road
from .util import array_to_qpointf

SCALE = 10.0 # pixel/meter
FPS = 60.0
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1200, 800)
        print("Hello MainWindow")
        #self.world = DummyWorld()
        self.world = World()
        self.camera = Camera()

        self.pan_last_pos = None
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(1000.0/FPS)
        self.world.dt = 1/FPS

    def on_timer(self):
        self.world.step()
        self.update()

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
            print(self.camera.center)
        return super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.pan_last_pos:
            pos = QVector2D(event.pos())
            v = pos - self.pan_last_pos
            #v.setY(-v.y())
            self.camera.center -= v/self.camera.scale
            self.update()
            self.pan_last_pos = pos

        return super().mouseMoveEvent(event)
    
class Camera:
    def __init__(self) -> None:
        self.center = QVector2D(500*SCALE, 500*SCALE)
        self.scale = 0.5

    def draw(self, painter: QPainter, world: World):
        viewport = painter.viewport()
        width = viewport.width()
        height = viewport.height()

        vp_transform = QTransform()
        vp_transform.translate(width/2, height/2)
        vp_transform.scale(1, 1)
        #vp_transform.scale(1, -1)

        camera_transform = QTransform()
        camera_transform.scale(self.scale, self.scale)
        camera_transform.translate(-self.center.x(), -self.center.y())

        transform = camera_transform * vp_transform

        painter.setTransform(transform)
        for road in world.get_roads():
            self.draw_road(road, painter)

        #print([car.pos for car in world.get_cars()])
        for car in world.get_cars():
            global_transform = self.get_transform(car)
            painter.setTransform(global_transform * transform)
            
            self.draw_car(car, painter)

    def draw_car(self, car: Car, painter: QPainter):
        painter.fillRect(-50, -15, 50, 30, "Grey")

        color = "Blue"
        if "special" in car.get_tags():
            color = "Red"      
        painter.fillRect(-20, -10, 10, 20, color)

        painter.drawPoint(0, 0)
        painter.drawText(0, 0, "{:.2f}".format(car.acc))

    def draw_road(self, road: Road, painter: QPainter):
        for line in road.get_lines():
            p1 = array_to_qpointf(line[0]*SCALE)
            p2 = array_to_qpointf(line[1]*SCALE)
            painter.drawLine(p1, p2)
    
    def get_transform(self, car: Car) -> QTransform:
        position = car.get_position()
        heading = car.get_heading()

        t = QTransform()
        t.translate(position[0]*SCALE, position[1]*SCALE)
        r = np.arctan2(*heading[::-1])
        t.rotateRadians(r)

        return t