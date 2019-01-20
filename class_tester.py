from Route import Route
from Vehicle import Vehicle
from RouteGraph import RouteGraph

speed = 18
battery_life = 4
charging_time = 27
scale = 20
start_t = (9, 2)
end_t = (-7, -8)
refill_t = ((7, 1), (8, 0), (5, -1), (1, -2), (2, -2), (0, -4), (-3, -5), (-5, -7), (-4, -3), (-6, -5))

route = Route(start_t, end_t, refill_t)
vehicle = Vehicle(speed, battery_life, charging_time)
route_graph = RouteGraph(route, vehicle, 20)
print(route_graph.get_edges_weight())
