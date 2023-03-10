from typing import Optional
from math import sqrt, pow
import numpy as np
from .util import Vec2
from .range import Range


class Car:
    def __init__(self, pos: float = 0.0, speed: float = 0.0):
        self.pos = pos
        self.speed = speed
        self.acc = 0.0
        self.length = 5.0
        self.position: Optional[Vec2] = None
        self.heading: Optional[Vec2] = None
        self.tag: dict = {}
        self.context: dict = {}

    def get_range(self) -> Range:
        return Range(self.pos - self.length, self.pos)

    def get_position(self) -> Optional[Vec2]:
        return self.position

    def get_heading(self) -> Optional[Vec2]:
        return self.heading

    def get_tags(self) -> dict:
        return self.tag

    def make_decision(self, dt: float):
        #print(self.context)
        gap = self.context["front_gap"]
        dv = self.context["approaching_speed"]
        self.acc = idm_car_following(gap, self.speed, dv)


    def execute_decision(self, dt: float):
        self.speed += self.acc
        self.pos += self.speed * dt + 0.5 * self.acc * dt * dt


def idm_car_following(
    gap, v, dv, v0=30.0, T=1.5, a=0.73, b=1.67, delta=4.0, s0=2.0
) -> float:
    s_star = s0 + v * T + v * dv / 2.0 / sqrt(a * b)
    factor = 1.0 - pow(v/v0, delta) - pow(s_star/gap, 2.0)
    
    return factor * a
