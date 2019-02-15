import optparse

from NMEA.NMEA import NMEA
from NMEA.visualization import make_graph_plot
from file_manipulation.txt_parse import txt_parse
from file_manipulation.pdf_create import make_pdf_report
from NMEA.Route import Route
from NMEA.Vehicle import Vehicle
from NMEA.RouteGraph import RouteGraph


def parser_init():
    parser = optparse.OptionParser(usage='NMEA_report_maker.py [options] [input_file] [output_path]')
    parser.add_option('-p', '--picture',
                      dest='picture',
                      action='store_true',
                      default=False,
                      help=("include graph picture "
                            "[default: off]"))
    return parser


def main():
    parser = parser_init()
    opts, args = parser.parse_args()
    input_file, output = args[0], args[1]
    data = txt_parse(input_file)
    route = Route(start=data['start point'],
                  end=data['final point'],
                  refill=data['refuel points'])
    vehicle = Vehicle(speed=data['speed(km/h)'],
                      battery_life=data['battery life(h)'],
                      charging_time=data['charging time(min)'])
    route_graph = RouteGraph(route, vehicle,
                             scale=data['scale(1:km)'])
    final_route = route_graph.get_short_route()
    edge_weights = route_graph.get_edges_weight()
    times = NMEA.get_times('12.25.00',
                           route_graph.get_edges_weight(),
                           vehicle.speed,
                           route_graph.get_short_route(),
                           vehicle.charging_time)
    angles = NMEA.get_angles(route_graph.coordinates,
                             route_graph.get_short_route())
    nmea_str = NMEA.get_nmeas(angles, times,
                              final_route, edge_weights)
    if opts.picture:
        make_graph_plot(route_graph.coordinates,
                        route_graph.adjacency, final_route,
                        data['scale(1:km)'], output)
    make_pdf_report(opts.picture, nmea_str, output)


if __name__ == '__main__':
    main()
