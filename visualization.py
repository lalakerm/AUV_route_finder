import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from class_tester import route_graph
from class_tester import scale

coordinates = route_graph.coordinates
adj_matrix = route_graph.adjacency
route = route_graph.get_short_route()

IMAGE = 'route_graph.png'
ROUTE_attr = {'color': 'blue', 'alpha': 0.8}
NON_ROUTE_EDGE_attr = {'color': 'red', 'linestyle': '--', 'alpha': 0.8}
VERTEX_attr = {'s': 270}
GRID_attr = {'which': 'both', 'alpha': 0.2}

plt.grid(b=True, **GRID_attr), plt.minorticks_on()

if route:
    for i in range(0, len(route)-1):  # route plot
        x = coordinates[route[i]-1][0], coordinates[route[i+1]-1][0]  # x = (x1,x2)
        y = coordinates[route[i]-1][1], coordinates[route[i+1]-1][1]  # y = (y1, y2)
        plt.plot(x, y, **ROUTE_attr)
adj_temp = np.ndarray.copy(adj_matrix)  # copy is needed to modify adj_matrix with mock values for route vertices
for i in range(0, len(route)-1):
    adj_temp[route[i]-1, route[i+1]-1] = adj_temp[route[i+1]-1, route[i]-1] = 0  # to prevent edges between route points
for i in range(0, len(adj_temp)):  # edges between non-route edges
    for j in range(0, len(adj_temp)):
        if adj_temp[i, j] == 1:
            adj_temp[j, i] = 0
            x = coordinates[i][0], coordinates[j][0]
            y = coordinates[i][1], coordinates[j][1]
            plt.plot(x, y, **NON_ROUTE_EDGE_attr)
for i, c in enumerate(coordinates):  # represent vertex as a point
    if i in (0, len(coordinates)-1):
        plt.scatter(*c, **VERTEX_attr, c='red', alpha=0.8)
    else:
        plt.scatter(*c, **VERTEX_attr, c='blue', alpha=0.2)
for i, c in enumerate(coordinates):  # add vertex number
    plt.annotate(str(i + 1), c, xytext=(c[0] - 0.15, c[1] - 0.15), fontsize=9)
legend_elements = [Line2D([0], [0], color='b', label='Optimal edge'),
                   Line2D([0], [0], color='r', linestyle='--', alpha=0.8, label='Non-optimal edge'),
                   Line2D([0], [0], marker='o', color='w',
                          markerfacecolor='red', markersize=9, alpha=0.8, label='Start(End) vertex'),
                   Line2D([0], [0], marker='o', color='w',
                          markerfacecolor='blue', markersize=9, alpha=0.2, label='Vertex')]
plt.legend(handles=legend_elements)
plt.text(plt.xlim()[1], plt.ylim()[1]+0.5, 'Scale 1:' + str(scale) + ' km', horizontalalignment='right',
         verticalalignment='top')
plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.savefig(IMAGE)
if os.path.isfile(os.getcwd() + '/output/' + IMAGE):
    os.remove(os.getcwd() + '/output/' + IMAGE)
os.rename(IMAGE, os.getcwd() + '/output/' + IMAGE)

