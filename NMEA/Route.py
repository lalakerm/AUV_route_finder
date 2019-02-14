"""

This module provide Route class to represent route model
with start, end points and possible refill points

"""


class Route:
    def __init__(self, start=(), end=(), refill=()):
        if len(start) != 2 or len(end) != 2:
            raise ValueError("Start and End should represent 2D-coordinate(ex. (3,2))")
        for e in refill:
            if len(e) != 2:
                raise ValueError("Refill should represent 2D-coordinate(ex. ((3,2),(2,3)) "
                                 "or a sequence of coordinates or empty sequence")
        self._start = start
        self._end = end
        self._refill = refill

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if len(value) == 2:
            self._start = value
        else:
            raise ValueError("Start should represent 2D-coordinate(ex. (3,2))")

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, value):
        if len(value) == 2:
            self._end = value
        else:
            raise ValueError("End should represent 2D-coordinate(ex. (3,2))")

    @property
    def refill(self):
        return self._refill

    @refill.setter
    def refill(self, value):
        if value == ():
            self._refill = value
        else:
            for e in value:
                if len(e) != 2:
                    raise ValueError("Refill should represent 2D-coordinate(ex. ((3,2),(2,3)) "
                                     "or a sequence of coordinates or empty sequence")
            self._refill = value
