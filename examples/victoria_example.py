
import pandas as pd

from inputs.classes import CsvInput
from components.digraphs import TemporalDiGraph
from plots.plotter import Plotter
from plots.circle import Circle
from plots.slice import Slice
from algorithms.foremost import calculate_foremost_tree


tube = TemporalDiGraph('TubeNetwork', data=CsvInput('./victoria.csv'))
tube.details()


station_df = pd.read_csv("stations_victoria.csv")

tube.nodes.add_data(station_df)

