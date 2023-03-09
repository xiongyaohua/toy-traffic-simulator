import numpy as np
from .car import Car
from .util import Vec2

class CenterLine:
    def __init__(self, p1: Vec2, p2: Vec2):
        self.p1 = p1
        self.p2 = p2

    def get_length(self):
        v = (self.p1 - self.p2).length()

    def tesselate(self) -> list:
        return [self.p1, self.p2]
    
    def sample_at(self, pos: float):
        v = (self.p2 - self.p1).normalized()
        p = self.p1 + pos * v
        return (p, v)

class Lane:
    def __init__(self, center_line):
        self.center_line: CenterLine = center_line
        self.cars = []

    def add_car(self, car: Car) -> bool:
        car.lane = self
        self.cars.append(car)
        return True
    
    def get_cars_in_range(self, position: float, length: float):
        raise NotImplementedError
    
    def update_context(self, dt):
        raise NotImplementedError
    
    def make_decision(self, dt):
        raise NotImplementedError
    
    def execute_decision(self, dt):
        for car in self.cars:
            car.move()
    