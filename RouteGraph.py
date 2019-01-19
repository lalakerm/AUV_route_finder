# RouteGraph represent route model in graph
import numpy as np

speed = 18
battery_life = 4
scale = 20
start_t = (9, 2)
end_t = (-7, -8)
refill_t = ((7, 1), (8, 0), (5, -1), (1, -2), (2, -2), (0, -4), (-3, -5), (-5, -7), (-4, -3), (-6, -5))


class RouteGraph:
    def __init__(self, start, end, refill=()):  # refill - set of points (x,y), start(end) - set (x,y)
        if len(refill):
            self.coordinates = np.vstack([np.array(start),
                                          np.vstack(refill),
                                          np.array(end)])
        else:
            self.coordinates = np.vstack([np.array(start),
                                          np.array(end)])
        self.adjacency = adj_matrix_comp(self.coordinates)

    def get_edges_weight(self):  # weights are equal to length from one point to another
        size = len(self.coordinates)
        edges_weight = np.zeros([size, size])  # matrix of edges weights
        for i in range(size):
            for j in range(size):
                if i == j:  # no distance from vertex to each self
                    pass
                elif self.adjacency[i, j] == 0:  # unreachable vertex ~ Inf distance -> Inf weight
                    edges_weight[i, j] = edges_weight[j, i] = np.Inf
                else:
                    distance = scale * np.linalg.norm(self.coordinates[j] - self.coordinates[i])
                    edges_weight[i, j] = edges_weight[j, i] = distance
        return edges_weight

    def get_short_route(self):
        edges_length = self.get_edges_weight()  # get matrix of edges weight
        size = len(edges_length)
        shortest_length = np.Inf * np.ones([size, size])  # i,j - shortest length to i vertex with no more than j edges
        shortest_length[0] = size * [0]  # shortest path from 1 to 1 vertices is 0
        # implementation of Bellman-Ford algorithm
        for k in range(0, size - 1):
            for m in range(0, size):
                for n in range(0, size):
                    if shortest_length[m, k] + edges_length[m, n] < shortest_length[n][k + 1:size]:
                        shortest_length[n, k + 1:size] = shortest_length[m, k] + edges_length[m, n]
        return shortest_length


def adj_matrix_comp(vertex_vector):  # computation of adjacency matrix with vector of vertex coordinates as input
    size = len(vertex_vector)
    adj_matrix = np.zeros([size, size], dtype=int)
    for i in range(size):
        for j in range(size):
            if i != j:  # avoid same vertices
                distance = np.linalg.norm(vertex_vector[i]-vertex_vector[j])  # distance between two vertices
                if distance * scale < speed * battery_life:  # if vertex is reachable
                    adj_matrix[i, j] = adj_matrix[j, i] = 1
    return adj_matrix
