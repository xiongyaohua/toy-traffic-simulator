from typing import Optional
import numpy as np
from .util import Vec2

class Car:
    def __init__(self, pos:float =0.0, speed:float =0.0):
        self.pos = pos
        self.speed = speed
        self.acc = 0.0
        self.length = 5.0
        self.position: Optional[Vec2] = None
        self.heading: Optional[Vec2] = None
        self.tag: dict = {}
        self.context: dict = {}

    def get_position(self) -> Optional[Vec2]:
        return self.position

    def get_heading(self) -> Optional[Vec2]:
        return self.heading

    def get_tags(self) -> dict:
        return self.tag

    def make_decision(self, dt:float):
        self.acc += 1.0*dt

    def execute_decision(self, dt:float):
        self.speed += self.acc
        self.pos += (self.speed * dt + 0.5 * self.acc * dt * dt)