
import overtime as ot

network = ot.TemporalDiGraph('SampleNetwork', data=ot.CsvInput('./data/network.csv'))

subgraph = network.get_temporal_subgraph(intervals=((0,3),(8,10)), nodes=('a', 'c', 'd'))
subgraph.details()
subgraph.print()
print(subgraph.edges.timespan())



plotter = ot.Plotter()
plotter.single(ot.Circle, network.get_snapshot(7))
plotter.single(ot.Slice, network)

snapshots = []
for t in network.edges.timespan():
    snapshots.append(network.get_snapshot(t))

plotter.multi(ot.Circle, snapshots)

a_tree = ot.calculate_foremost_tree(network, 'a')
print(ot.calculate_reachability(network, 'a'))
plotter.single(ot.Circle, a_tree)

input("Press enter key to exit...")
