
import overtime as ot
import pandas as pd


tube = ot.TemporalDiGraph('TubeNetwork', data=ot.CsvInput('./bakerloo-inbound.csv'))
tube.details()

ot.Circle(tube)
plotter = ot.Plotter()
plotter.single(ot.Circle, tube)
ot.Slice(tube)

for node in tube.nodes.set:
    node.data['reachability'] = ot.calculate_reachability(tube, node.label)

ot.NodeScatter(tube, bubble_metric='reachability')

station_df = pd.read_csv("bakerloo-stations.csv")
tube.nodes.add_data(station_df)

ot.NodeScatter(tube, x='lon', y='lat', bubble_metric='reachability')

foremost_oxcirc = ot.calculate_foremost_tree(tube, 'Oxford Circus')
foremost_oxcirc.nodes.add_data(station_df)
ot.NodeScatter(foremost_oxcirc, x='lon', y='lat', bubble_metric='foremost_time')


input("Press enter key to exit...")
