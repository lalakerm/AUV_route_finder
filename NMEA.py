# Represent NMEA message as an object
import numpy as np
import datetime


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


def get_times(start_time, edges_weight, speed, route, charging_time):  # start_time format HH.MM.SS
    times = list()
    time = datetime.time(*list(map(int, start_time.split('.'))))
    time_matrix = np.copy(edges_weight)
    for i in range(0, len(time_matrix)):
        for j in range(0, len(time_matrix)):
            time_matrix[i, j] /= (speed / 60)  # 60 to get minutes in time_matrix
    for i in range(len(route) - 1, 0, -1):
        add_minutes = time_matrix[route[i] - 1, route[i - 1] - 1]  # minutes to add to current time
        time = (datetime.datetime.combine(datetime.date(1, 1, 1), time)
                + datetime.timedelta(
                    minutes=add_minutes + charging_time)).time()  # time of arrival+charging at the vertex
        times.append(time)
    return times
