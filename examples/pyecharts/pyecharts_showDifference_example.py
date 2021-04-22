import overtime as ot
from pyecharts.charts import Page


# load data (simple network)
network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../../overtime/data/network.csv'))

# load data (London subway stations - Victoria)
tfl_data = ot.CsvInput('../../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
network2.nodes.add_data('../../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

ot.ShowDifference(network1, 'c', 3, layout='circular', graph_layout=ot.generate_Layout(network1), pageLayout=Page.DraggablePageLayout,path='../html/showDifference_circular_layout.html')

ot.ShowDifference(network1, 'h', 3, layout='force', graph_layout=ot.generate_Layout(network1),pageLayout=Page.DraggablePageLayout,path='../html/showDifference_force_layout.html')

ot.ShowDifference(network2, 'c',100, x='lon',y='lat', layout='location', graph_layout=ot.generate_Layout(network2),show_edge_value=False, pageLayout=Page.DraggablePageLayout,path='../html/showDifference_location_layout.html')












