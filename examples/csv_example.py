
from inputs.classes import CsvInput
from components.digraphs import TemporalDiGraph
from plots.plotter import Plotter
from plots.circle import Circle
from plots.slice import Slice


graph = TemporalDiGraph('TestNetwork1', data=CsvInput('./network.csv'))
graph.details()

graph.add_node('x')
graph.add_edge('f', 'a', 3, 7)

plotter = Plotter()
plotter.single(Circle, graph)
plotter.single(Slice, graph, save=True)


snapshots = []
for t in graph.edges.timespan():
    snapshots.append(graph.get_snapshot(t))

plotter.multi(Circle, snapshots, save=True)


input("Press enter key to exit...")
