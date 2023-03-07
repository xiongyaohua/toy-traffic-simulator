from PySide6.QtGui import QVector2D, QTransform
import numpy as np

class Car:
    def __init__(self, pos=0.0, speed=0.0):
        self.pos = pos
        self.speed = speed
        self.acc = 0.0
        self.lane: Lane = None

    def get_position(self) -> QVector2D:
        if self.lane:
            p, v = self.lane.center_line.sample_at(self.pos)
            return p

    def get_heading(self) -> QVector2D:
        if self.lane:
            p, v = self.lane.center_line.sample_at(self.pos)
            return v

    def get_transform(self) -> QTransform:
        position = self.get_position()
        heading = self.get_heading()
        t = QTransform()
        t.translate(*position.toTuple())
        r = np.arctan2(*heading.toTuple()[::-1])
        t.rotateRadians(r)

        return t
    
    def get_tags(self) -> dict:
        raise NotImplementedError
    
    def move(self, dt):
        self.pos = self.pos + self.speed * dt + 0.5 * self.acc * dt * dt
