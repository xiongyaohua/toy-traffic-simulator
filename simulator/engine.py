from typing import Sequence
import numpy as np

from .util import Vec2, vec2_to_array
from .lane import Lane
from .car import Car
from .road import Road
from .world import World


class DummyCar(Car):
    def __init__(self, x, y, dx, dy):
        self.position = (x, y)
        self.heading = (dx, dy)
        self.tags = {}

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
