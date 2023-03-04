from typing import Sequence
import numpy as np
from PySide6.QtGui import QVector2D, QTransform

from .lane import Lane
from .car import Car
from .road import Road


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
        self.tags = {}

    def get_position(self) -> QVector2D:
        return self.position

    def get_heading(self) -> QVector2D:
        return self.heading

    def get_tags(self):
        return self.tags
    
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

        car = DummyCar(400, 200, 0, 1)
        car.tags["special"] = True
        self.cars.append(car)
