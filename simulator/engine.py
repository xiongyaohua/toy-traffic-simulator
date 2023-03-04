from typing import Sequence
import numpy as np
from PySide6.QtGui import QVector2D, QTransform


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
        r = np.arctan2(*heading.toTuple())
        t.rotateRadians(r)

        return t

class Road:
    pass


class World:
    def __init__(self):
        pass

    def get_cars(self) -> Sequence[Car]:
        raise NotImplementedError

    def get_roads(self) -> Sequence[Road]:
        raise NotADirectoryError


class DummyCar(Car):
    def __init__(self, x, y, dx, dy):
        self.position = QVector2D(x, y)
        self.heading = QVector2D(dx, dy).normalized()

    def get_position(self) -> QVector2D:
        return self.position

    def get_heading(self) -> QVector2D:
        return self.heading


class DummyWorld(World):
    def __init__(self, n: int = 100, w: float = 1000, h: float = 800):
        self.n = n
        self.w = w
        self.h = h
        self._generate_cars()

    def get_cars(self) -> Sequence[Car]:
        return self.cars

    def _generate_cars(self):
        xs = np.random.rand(self.n) * self.w
        ys = np.random.rand(self.n) * self.h
        rs = np.random.rand(self.n) * np.pi * 2.0

        self.cars = []

        for x, y, r in zip(xs, ys, rs):
            car = DummyCar(x, y, np.cos(r), np.sin(r))
            self.cars.append(car)
