import numpy as np
from numpy.linalg import norm
from .util import Vec2, vec2_to_array

POINTS_AROUND_CIRCLE = 144

class CenterLine:
    def __init__(self, points=[]):
        self.segments = []
        if len(points) >= 2:
            self._make_segments(points)

    def _make_segments(self, points):
        segments = []
        for p1, p2 in zip(points[:-1], points[1:]):
            line = Line(p1, p2)
            segments.append(line)

        self.segments = segments

    def get_length(self):
        return sum([s.get_length() for s in self.segments])

    def tesselate(self) -> list:
        n = len(self.segments)
        if n == 0:
            return []
        elif n == 1:
            return self.segments[0].tesselate()
        else:
            points = []
            points.extend(self.segments[0].tesselate())
            for i in range(1, n):
                points.extend(self.segments[i].tesselate()[:-1])
            return points
    
    def sample_at(self, pos: float):
        assert pos >= 0.0 and pos <= self.get_length()
        for s in self.segments:
            if pos <= s.get_length():
                return s.sample_at(pos)
            else:
                pos -= s.get_length()

    def get_offseted(self, offset):
        segments = [s.get_offseted(offset) for s in self.segments]
        ct = CenterLine()
        ct.segments = segments
        return ct

class Arc:
    def __init__(self, center: Vec2, r:float, a:float, da:float):
        self.center = vec2_to_array(center)
        self.r = r
        self.a = a
        self.da = da
        self.length = self.r * abs(self.da)

    def get_length(self):
        return self.length
    
    def sample_at(self, pos: float) -> tuple:
        assert pos >= 0.0 and pos <= self.length
        a = self.a + pos / self.length * self.da
        normal: np.ndarray = np.array([np.cos(a), np.sin(a)])
        
        if self.da > 0.0:
            tangent = np.array([-normal[1], normal[0]])
        else:
            tangent = np.array([normal[1], -normal[0]])
        p = self.center + self.r * normal

        return (p, tangent)
    
    def tesselate(self) -> list:
        n = int(self.da / 2.0 / np.pi * 144)
        if n < 2:
            n = 2

        points = []
        ida = self.da / (n - 1)
        for i in range(n):
            a = self.a + ida * i
            normal: np.ndarray = np.array([np.cos(a), np.sin(a)])
            p = self.center + self.r * normal
            points.append(p)

        return points
    
    def get_offseted(self, offset):
        assert offset < self.r

        return Arc(self.center, self.r+offset, self.a, self.da)

class Line:
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
    
    def get_offseted(self, offset):
        p1 = self.p1 + self.normal * offset
        p2 = self.p2 + self.normal * offset
        return Line(p1, p2)
        