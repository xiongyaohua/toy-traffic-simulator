from PySide6.QtGui import QVector2D, QTransform
import numpy as np

class Car:
    def get_position(self) -> QVector2D:
        raise NotImplementedError

    def get_heading(self) -> QVector2D:
        raise NotImplementedError

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
