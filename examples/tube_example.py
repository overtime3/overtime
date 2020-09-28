
from inputs.classes import CsvInput
from components.digraphs import TemporalDiGraph
from plots.plotter import Plotter
from plots.circle import Circle
from plots.slice import Slice
from algorithms.foremost import calculate_foremost_tree


tube = TemporalDiGraph('TubeNetwork', data=CsvInput('./tube.csv'))
tube.details()

plotter = Plotter()
# plotter.single(Circle, tube.get_temporal_subgraph((840, 860)), ordered=True, save=True)
# plotter.single(Circle, calculate_foremost_tree(tube.get_temporal_subgraph((840, 860)), 'Blackhorse Road'), ordered=True, save=True)
# plotter.single(Slice, calculate_foremost_tree(tube.get_temporal_subgraph((840, 860)), 'Blackhorse Road'), slider=True, save=True)
plotter.single(Circle, calculate_foremost_tree(tube.get_temporal_subgraph((850, 920)), 'Warren Street'), ordered=True, save=True)
# plotter.single(Circle, tube, save=True)
# plotter.single(Slice, tube, save=False)

input("Press enter key to exit...")
