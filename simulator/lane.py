import numpy as np
from PySide6.QtGui import QVector2D
from .car import Car

class CenterLine:
    def __init__(self, p1: QVector2D, p2: QVector2D):
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
        self.center_line = center_line

    def get_center_line(self):
        return self.center_line

    def insert_car(self, car: Car) -> bool:
        raise NotImplementedError
    
    def get_cars_in_range(self, position: float, length: float):
        raise NotImplementedError
    
    def update_context(self, dt):
        raise NotImplementedError
    
    def make_decision(self, dt):
        raise NotImplementedError
    
    def execute_decision(self, dt):
        raise NotImplementedError
    
class CellunaAutomataLane(Lane):
    def __init__(self, center_line: CenterLine, cell_length: float):
        super().__init__(center_line)
        self.num_cells = int(center_line.get_length() / cell_length)
        if self.num_cells == 0:
            self.num_cells = 1

        self.cell_length = center_line.get_length() / self.num_cells

        self.cells = [None] * self.cell_length