from typing import Sequence, Optional
import numpy as np
from numpy.linalg import norm
from .car import Car
from .util import Vec2, vec2_to_array

class CenterLine:
    def __init__(self, p1: Vec2, p2: Vec2):
        self.p1 = vec2_to_array(p1)
        self.p2 = vec2_to_array(p2)
        self.length = norm(self.p1 - self.p2)
        self.tangent = (self.p2 - self.p1) / self.length
        self.normal = np.array([self.tangent[1], -self.tangent[0]])

    def get_length(self):
        return self.length

    def tesselate(self) -> list:
        return [self.p1, self.p2]
    
    def sample_at(self, pos: float) -> tuple[Vec2, Vec2]:
        p = self.p1 + pos * self.tangent
        return (p, self.tangent)
    
    def get_offseted(self, offset) -> CenterLine:
        p1 = self.p1 + self.normal * offset
        p2 = self.p2 + self.normal * offset
        return CenterLine(p1, p2)

class Lane:
    def __init__(self, center_line: CenterLine):
        self.center_line = center_line
        self.length = self.center_line.get_length()
        self.cars: list[Car] = []

    def add_car(self, car: Car) -> bool:
        self.cars.append(car)
        return True
    
    def get_cars(self) -> Sequence[Car]:
        for car in self.cars:
            p, v = self.center_line.sample_at(car.pos)
            car.position = p
            car.heading = v
        return self.cars
    
    def get_leading_car(self) -> Optional[Car]:
        if self.cars:
            return self.cars[-1]
        else:
            return None
        
    def is_range_empty(self, f, t) -> bool:
        pass
    
    def update_context(self, dt):
        self.cars.sort(key=lambda car: car.pos)

        n = len(self.cars)
        if n >= 1:
            for car, next_car in zip(self.cars[:-1], self.cars[1:]):
                car.context["front_gap"] = next_car.pos - car.pos - next_car.length
            self.cars[-1].context["front_gap"] = 1000.0
    
    def make_decision(self, dt):
        for car in self.cars:
            car.make_decision(dt)
    
    def execute_decision(self, dt):
        for car in self.cars:
            car.execute_decision(dt)
    