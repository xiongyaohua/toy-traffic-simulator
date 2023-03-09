import numpy as np
from .util import Vec2

class Car:
    def __init__(self, pos:float =0.0, speed:float =0.0):
        self.pos = pos
        self.speed = speed
        self.acc = 0.0

    def get_position(self) -> Vec2:
        raise NotImplementedError

    def get_heading(self) -> Vec2:
        raise NotImplementedError

    def get_tags(self) -> dict:
        raise NotImplementedError
    
    def move(self, dt):
        self.pos = self.pos + self.speed * dt + 0.5 * self.acc * dt * dt
