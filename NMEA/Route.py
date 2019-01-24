# Class represent route with start,end points and refuel_points
class Route:
    def __init__(self, start, end, refill=()):
        self.start = start
        self.end = end
        self.refill = refill
