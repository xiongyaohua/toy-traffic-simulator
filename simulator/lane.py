from typing import Sequence, Optional
from .car import Car
from .range import Range
from .center_line import CenterLine

class Lane:
    def __init__(self, center_line: CenterLine):
        self.center_line = center_line
        self.length = self.center_line.get_length()
        self.cars: list[Car] = []

    def add_car(self, car: Car) -> bool:
        self.cars.append(car)
        self.cars.sort(key=lambda car: car.pos)
        
        return True
    
    def add_cars(self, cars:Sequence[Car]) -> bool:
        self.cars.extend(cars)
        self.cars.sort(key=lambda car: car.pos)
        
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
        
    def is_range_clear(self, back, front) -> bool:
        range = Range(back, front)
        return _is_range_clear(range, self.cars)
    
    def update_context(self, dt):
        # Assume cars sorted by pos
        n = len(self.cars)
        if n >= 1:
            for car, front_car in zip(self.cars[:-1], self.cars[1:]):
                car.context["front_gap"] = front_car.pos - car.pos - front_car.length
                car.context["approaching_speed"] = car.speed - front_car.speed
            self.cars[-1].context["front_gap"] = 1000.0
            self.cars[-1].context["approaching_speed"] = 0.0
    
    def make_decision(self, dt):
        for car in self.cars:
            car.make_decision(dt)
    
    def execute_decision(self, dt):
        for car in self.cars:
            car.execute_decision(dt)
    
def _is_range_clear(range: Range, cars:list[Car]) -> bool:
    if len(cars) <= 5:
        # Linear search for sort list
        for car in cars:
            cr = car.get_range()
            if range.intersect(cr):
                return False
        else:
            return True
    else:
        # Bi-section search for long list
        l = len(cars)
        mid = l // 2
        cr = cars[mid].get_range()
        if range.intersect(cr):
            return False
        else:
            if cr.back >= range.front:
                return _is_range_clear(range, cars[mid+1:])
            else:
                return _is_range_clear(range, cars[:mid])

