# Represent NMEA message as an object
import numpy as np


class NMEA:

    NMEA_template = '$UTHDG,{time},{dist},T,{angle},{is_end}'

    def __init__(self, time, dist, turn, angle):
        self.time = time
        self.dist = dist
        self.turn = turn
        self.angle = angle


def get_angles(coordinates, route=()):
    angles = []
    for i in range(len(route) - 1, 0, -1):
        # coordinates of vertexes to find angle
        x1, y1 = coordinates[route[i] - 1]
        x2, y2 = coordinates[route[i - 1] - 1]
        # dx and dy to determine direction
        dx = (x2 - x1)
        dy = (y2 - y1)
        angle = np.abs(np.degrees(np.arcsin(dy / np.linalg.norm((dx, dy)))))
        if dy >= 0:
            a = 180 - angle if dx <= 0 else angle
        elif dy <= 0:
            a = 180 + angle if dx <= 0 else 360 - angle
        angles.append(a)
    return angles


def get_times(edge_weight, route, charging_time, speed):
    pass
