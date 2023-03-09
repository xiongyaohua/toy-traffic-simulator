from typing import Sequence
from .util import Vec2
from .lane import CenterLine, Lane
from .car import Car

LANE_WIDTH = 3.5

class Source:
    def __init__(self, q=0.5):
        self.q = q
        self.pending: list[Car] = []
        self.remain_time = 0.0

    def step(self, dt):
        self.remain_time -= dt
        while dt < 0.0:
            self.pending.append(Car())
            dt += 2.0

class Road:
    def __init__(self, p1: Vec2, p2: Vec2, nlane=3):
        self.center_line = CenterLine(p1, p2)
        self.length = self.center_line.get_length()

        self.lanes:list[Lane] = []
        total_width = nlane * LANE_WIDTH
        left_edge_offset = -total_width / 2.0
        left_center_offset = left_edge_offset + 0.5 * LANE_WIDTH
        
        self.source = Source()

        for i in range(3):
            offset = left_center_offset + i * LANE_WIDTH
            center_line = self.center_line.get_offseted(offset)
            lane = Lane(center_line)
            self.lanes.append(lane)

    def get_cars(self) -> Sequence[Car]:
        cars: list[Car] = []
        for lane in self.lanes:
            cars.extend(lane.get_cars())

        return cars
    
    def update_context(self, dt):
        for lane in self.lanes:
            lane.update_context(dt)
    
    def make_decision(self, dt):
        for lane in self.lanes:
            lane.make_decision(dt)
    
    def execute_decision(self, dt):
        for lane in self.lanes:
            lane.execute_decision(dt)

    def update_boundary(self, dt):
        for lane in self.lanes:
            car = lane.get_leading_car()
            if car and car.pos > lane.length:
                lane.cars.remove(car)

        self.source.step(dt)
        
        



        