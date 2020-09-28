
from inputs.classes import CsvInput
from components.digraphs import TemporalDiGraph
from algorithms.foremost import calculate_foremost_tree

from plots.plotter import Plotter
from plots.circle import Circle


graph = TemporalDiGraph('TestNetwork', data=CsvInput('./network.csv'))

myplotter = Plotter()
myplotter.single(Circle, graph)

myplotter.single(Circle, graph.get_snapshot(7))
myplotter.multi(Circle, [graph.get_snapshot(4), graph.get_snapshot(7)])

myplotter.multi(Circle,
    [
        graph.get_temporal_subgraph((0, 7)),
        graph.get_temporal_subgraph((7, 14))
    ]
)

myplotter.multi(
    Circle,
    [
        calculate_foremost_tree(graph, 'a'),
        calculate_foremost_tree(graph, 'b'),
        calculate_foremost_tree(graph, 'c'),
        calculate_foremost_tree(graph, 'd'),
        calculate_foremost_tree(graph, 'e')
    ]
)

myplotter.single(Circle, calculate_foremost_tree(graph.get_temporal_subgraph((0,7)), 'a'))

input("Press enter key to exit...")
