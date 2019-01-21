from Route import Route
from Vehicle import Vehicle
from RouteGraph import RouteGraph
import NMEA

speed = 18
battery_life = 4
charging_time = 27
scale = 20
start_t = (9, 2)
end_t = (-7, -8)
refill_t = ((7, 1), (8, 0), (5, -1), (1, -2), (2, -2), (0, -4), (-3, -5), (-5, -7), (-4, -3), (-6, -5))

route = Route(start_t, end_t, refill_t)
vehicle = Vehicle(speed, battery_life, charging_time)
route_graph = RouteGraph(route, vehicle, scale=scale)
final_route = route_graph.get_short_route()
edge_weights = route_graph.get_edges_weight()
times = NMEA.get_times('12.25.00', route_graph.get_edges_weight(), vehicle.speed, route_graph.get_short_route(),
                       vehicle.charging_time)
angles = NMEA.get_angles(route_graph.coordinates, route_graph.get_short_route())
nmea_list = list()
for i, t in enumerate(times):
    a = angles[i]
    final_route_inv = list.copy(final_route)  # copy final_route to avoid changes to original
    final_route_inv.reverse()
    matrix_ind = final_route[i]-1, final_route[i+1]-1  # index of edge_weights matrix
    if i == len(times) - 1:
        nmea = NMEA.NMEA(t,  edge_weights[matrix_ind], a)
    else:  # end of the route
        nmea = NMEA.NMEA(t,  edge_weights[matrix_ind], a, is_end=True)
    nmea_list.append(nmea)
nmea_str = tuple(str(nmea) for nmea in nmea_list)
