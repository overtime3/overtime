import overtime as ot
from pyecharts.charts import Page


# load data (simple network)
network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../../overtime/data/network.csv'))

# load data (London subway stations - Victoria)
tfl_data = ot.CsvInput('../../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
network2.nodes.add_data('../../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

# location layout
# London subway stations - Victoria
# don't show edge value
ot.echarts_Location(network2,100,'lon','lat',show_edge_value=False,path='../html/network_location_layout1.html', title='location layout', subtitle='London subway stations')

# location layout
# London subway stations - Victoria
# show edge value
ot.echarts_Location(network2,100,'lon','lat',path='../html/network_location_layout2.html', title='location layout', subtitle='London subway stations', pageLayout=Page.DraggablePageLayout)

