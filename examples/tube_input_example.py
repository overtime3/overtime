
from inputs.classes import TflInput
from components.digraphs import TemporalDiGraph
from plots.plotter import Plotter
from plots.circle import Circle
from plots.slice import Slice
from algorithms.foremost import calculate_foremost_tree


tube_input = TflInput(['victoria', 'bakerloo'], ['1600'])

tube = TemporalDiGraph('TubeNetwork', data=tube_input)
tube.details()


# plotter = Plotter()
# plotter.single(Slice, tube, slider=False)
# plotter.single(Circle, calculate_foremost_tree(tube, 'Holborn'))
# plotter.single(Slice, calculate_foremost_tree(tube, 'Holborn'))

input("Press enter key to exit...")
