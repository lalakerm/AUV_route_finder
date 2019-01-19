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

    def get_edges_length(self):
        size = len(self.coordinates)
        edges_length = np.zeros([size, size])  # matrix of edges lengths
        for i in range(size):
            for j in range(size):
                if i == j:  # no distance from vertex to each self
                    pass
                elif self.adjacency[i, j] == 0:
                    edges_length[i, j] = edges_length[j, i] = np.Inf
                else:
                    distance = scale * np.linalg.norm(self.coordinates[j] - self.coordinates[i])
                    edges_length[i, j] = edges_length[j, i] = distance
        return edges_length


def adj_matrix_comp(vertex_vector):  # computation of adjacency matrix with vector of vertex coordinates as input
    size = len(vertex_vector)
    adj_matrix = np.zeros([size, size], dtype=int)
    for i in range(size):
        for j in range(size):
            if i != j:  # avoid same vertices
                distance = np.linalg.norm(vertex_vector[i]-vertex_vector[j]) # distance between two vertices
                if distance * scale < speed * battery_life:  # if vertex is reachable
                    adj_matrix[i, j] = adj_matrix[j, i] = 1
    return adj_matrix
