"""
This module provides NMEA class for a single message,
NMEA object consist of time, distance, angle and boolean variable
to determine if message is last.
"""
import numpy as np
import datetime


class NMEA:
    NMEA_template = '$UTHDG,{time},{dist:.2f},T,{angle:.2f},{is_end}'

    def __init__(self, time, dist, angle, is_end=False):
        self._time = time
        self._dist = dist
        self._is_end = is_end
        self._angle = angle

    def __str__(self):
        if self._is_end:
            return NMEA.NMEA_template.format(time=self._time, dist=self._dist, angle=self._angle, is_end='E')
        else:
            return NMEA.NMEA_template.format(time=self._time, dist=self._dist, angle=self._angle, is_end='N')

    @staticmethod
    def get_angles(coordinates, route=()):
        """
        Returns tuple of angles, that's used to form NMEA message, depending on the route

        >>> coordinates=((0, 0), (1, 0), (-1, 0))
        >>> route=[3,2,1]
        >>> NMEA.get_angles(coordinates, route)
        [0.0, 180.0]
        """
        angles = []
        for i in range(len(route) - 1, 0, -1):
            # coordinates of vertexes to find angle
            x1, y1 = coordinates[route[i] - 1]
            x2, y2 = coordinates[route[i - 1] - 1]
            # dx and dy to determine direction
            dx = (x2 - x1)
            dy = (y2 - y1)
            angle = np.abs(np.degrees(np.arcsin(dy / np.linalg.norm((dx, dy)))))  # get absolute value of angle
            if dy >= 0:  # determine direction
                a = 180 - angle if dx <= 0 else angle
            elif dy <= 0:
                a = 180 + angle if dx <= 0 else 360 - angle
            angles.append(a)
        return angles

    @staticmethod
    def get_nmeas(angles, times, final_route, edge_weights):
        """
        Return list of NMEAs with given angles, times, final route and edge weights

        >>> angles=[0.0, 180.0]
        >>> times=(datetime.time(10,0,0), datetime.time(11,0,0))
        >>> final_route=[3,2,1]
        >>> edge_weights=np.ones([3,3])
        >>> NMEA.get_nmeas(angles, times, final_route, edge_weights)
        ('$UTHDG,10:00:00,1.00,T,0.00,E', '$UTHDG,11:00:00,1.00,T,180.00,N')
        """
        nmea_list = list()
        for i, t in enumerate(times):
            a = angles[i]
            final_route_inv = list.copy(final_route)  # copy final_route to avoid changes to original
            final_route_inv.reverse()
            matrix_ind = final_route[i] - 1, final_route[i + 1] - 1  # index of edge_weights matrix
            if i == len(times) - 1:
                nmea = NMEA(t, edge_weights[matrix_ind], a)
            else:  # end of the route
                nmea = NMEA(t, edge_weights[matrix_ind], a, is_end=True)
            nmea_list.append(nmea)
        nmea_str = tuple(str(nmea) for nmea in nmea_list)
        return nmea_str

    @staticmethod
    def get_times(start_time, edges_weight, speed, route, charging_time):  # start_time format HH.MM.SS
        """
        Returns tuple of times, that's used to form NMEA message, depending on the route

        >>> start_time = '12.25.00'
        >>> edges_weight = np.ones([3,3])
        >>> speed = 10
        >>> route = [3,2,1]
        >>> charging_time = 5
        >>> NMEA.get_times(start_time, edges_weight, speed, route, charging_time)
        [datetime.time(12, 36), datetime.time(12, 47)]
        """
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
            time = time.replace(microsecond=0)
            times.append(time)
        return times


if __name__ == "__main__":
    import doctest
    doctest.testmod()
