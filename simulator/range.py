class Range:
    def __init__(self, back, front):
        assert front > back
        self.back = back
        self.front = front

    def intersect(self, other):
        if self.back >= other.front or other.back >= self.front:
            return None
        
        back = max(self.back, other.back)
        front = min(self.front, other.front)

        return Range(back, front)
