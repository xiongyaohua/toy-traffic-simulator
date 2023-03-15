from typing import Sequence
from .car import Car
from .road import Road

class World:
    def __init__(self):
        self.roads: list[Road] = []
        self.time = 0.0
        self.dt = 0.1

        road = Road([(100,100), (500, 500), (500, 1000)])
        self.roads.append(road)

    def get_cars(self) -> Sequence[Car]:
        cars: list[Car] = []
        for road in self.roads:
            cars.extend(road.get_cars())

        return cars

    def get_roads(self) -> Sequence[Road]:
        return self.roads
    
    def step(self):
        for road in self.roads:
            road.update_context(self.dt)
        for road in self.roads:
            road.make_decision(self.dt)
        for road in self.roads:
            road.execute_decision(self.dt)
        for road in self.roads:
            road.update_boundary(self.dt)
            
        self.time += self.dt
