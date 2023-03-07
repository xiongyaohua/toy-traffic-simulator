from typing import Sequence
from .car import Car
from .road import Road

class World:
    def __init__(self):
        pass

    def get_cars(self) -> Sequence[Car]:
        raise NotImplementedError

    def get_roads(self) -> Sequence[Road]:
        raise NotADirectoryError
