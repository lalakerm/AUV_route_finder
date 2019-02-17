"""
This module provides Route Graph class, that
allows to represent graph model(as an adjacency matrix),
that's used to find optimal route among all the other possible.
"""
import numpy as np


class RouteGraph:
    def __init__(self, route, vehicle, scale=1):  # refill - set of points (x,y), start(end) - set (x,y)
        if len(route.refill):
            self._coordinates = np.vstack([np.array(route.start),
                                          np.vstack(route.refill),
                                          np.array(route.end)])
        else:
            self._coordinates = np.vstack([np.array(route.start),
                                          np.array(route.end)])
        self._scale = scale
        self._adjacency = self.adj_matrix_comp(self._coordinates,
                                               vehicle.speed,
                                               vehicle.battery_life,
                                               self._scale)

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def adjacency(self):
        return self._adjacency

    def get_edges_weight(self):
        """

        Return matrix of edges weights, which are equal to length
        from one vertex to another

        """
        # weights are equal to length from one vertex to another
        size = len(self._coordinates)
        edges_weight = np.zeros([size, size])  # matrix of edges weights
        for i in range(size):
            for j in range(size):
                if i == j:  # no distance from vertex to each self
                    pass
                elif self._adjacency[i, j] == 0:  # unreachable vertex ~ Inf distance -> Inf weight
                    edges_weight[i, j] = edges_weight[j, i] = np.Inf
                else:
                    distance = self._scale * np.linalg.norm(self._coordinates[j] - self._coordinates[i])
                    edges_weight[i, j] = edges_weight[j, i] = distance
        return edges_weight

    def get_short_route(self, log=False):
        """

        Return shortest route from start to end using Bellman-Ford algorithm,
        with optional log opportunity.

        """
        final_route = list()
        edges_length = self.get_edges_weight()  # get matrix of edges weight
        size = len(edges_length)
        shortest_length = np.Inf * np.ones([size, size])  # i,j - shortest length to i vertex with no more than j edges
        shortest_length[0] = size * [0]  # shortest path from 1 to 1 vertices is 0
        # implementation of Bellman-Ford algorithm
        for k in range(0, size - 1):
            for m in range(0, size):
                for n in range(0, size):
                    if (shortest_length[m, k] + edges_length[m, n] < shortest_length[n][k + 1:size]).all():
                        shortest_length[n, k + 1:size] = shortest_length[m, k] + edges_length[m, n]
        # route to final exist => last row of shortest_length matrix has at least one numeric value
        if np.array_equal(shortest_length[size - 1], size * [np.Inf]):
            return tuple(final_route)  # tuple cast to avoid changes
        else:  # final route computation (from final to start)
            final_route.append(size)  # size == final vertex
            min_distance = min(shortest_length[size - 1])  # min dist on last row of shortest_length matrix
            comp_coord = size - 1
            # -1 in range() so that i,j might be equal to 0
            for i in range(size-1, -1, -1):
                for j in range(size - 1, -1, -1):
                    if np.isclose(min_distance, (shortest_length[j, i] + edges_length[j, comp_coord])) \
                            and edges_length[j, comp_coord] != 0:
                        final_route.append(j+1)
                        min_distance = shortest_length[j, i]
                        comp_coord = j
                        break
        return (final_route, shortest_length) if log else final_route

    @staticmethod
    # computation of adjacency matrix with vector of vertex coordinates as input
    def adj_matrix_comp(vertex_vector, speed, battery_life, scale):
        """

        Return graph representation as a adjacency matrix

        >>> battery_life = 5
        >>> scale = 10
        >>> size = 10
        >>> speed = 15
        >>> vertex_vector = np.array([[10, 10], [8, 8], [5,5]])
        >>> RouteGraph.adj_matrix_comp(vertex_vector, speed, battery_life, scale)
        array([[0, 1, 1],
               [1, 0, 1],
               [1, 1, 0]])
        """
        size = len(vertex_vector)
        adj_matrix = np.zeros([size, size], dtype=int)
        for i in range(size):
            for j in range(size):
                if i != j:  # avoid same vertices
                    distance = np.linalg.norm(vertex_vector[i] - vertex_vector[j])  # distance between two vertices
                    if distance * scale < speed * battery_life:  # if vertex is reachable
                        adj_matrix[i, j] = adj_matrix[j, i] = 1
        return adj_matrix
