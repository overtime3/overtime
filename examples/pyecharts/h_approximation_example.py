import overtime as ot


# load data (simple network)
network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../../overtime/data/network.csv'))

# load data (London subway stations - Victoria)
tfl_data = ot.CsvInput('../../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
network2.nodes.add_data('../../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

ot.h_approximation(network1, 3)
# render the image after running h-approximation algorithm
# circular layout
ot.echarts_Circular(network1,3,path='../html/simple_network_h-approximation.html',title='simple network after h-approximation algorithm', subtitle='simple network (h=3)')

ot.h_approximation(network2, 100)
# render the image after running h-approximation algorithm
# location layout
ot.echarts_Location(network2,100,'lon','lat',show_edge_value=False, path='../html/London_subway_stations_h-approximation_location.html',title='London subway stations network after h-approximation algorithm', subtitle='London subway stations (h=100)')


