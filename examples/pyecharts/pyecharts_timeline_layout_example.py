import overtime as ot


# load data (simple network)
network1 = ot.TemporalDiGraph('test_network', data=ot.CsvInput('../../overtime/data/network.csv'))

# load data (London subway stations - Victoria)
tfl_data = ot.CsvInput('../../overtime/data/victoria_central_bakerloo_piccadilly-inbound_outbound.csv')
network2 = ot.TemporalDiGraph('TflNetwork', data=tfl_data)
network2.nodes.add_data('../../overtime/data/victoria_central_bakerloo_piccadilly-stations.csv')

# timeline - circular layout
# simple network
ot.echarts_Timeline(network1,3,path='../html/network_circular_layout_timeline1.html', title='circular layout timeline', subtitle='simple network',layout='circular')

# timeline - force layout
# simple network
ot.echarts_Timeline(network1,3,path='../html/network_force_layout_timeline2.html', title='force layout timeline', subtitle='simple network',layout='force')

# timeline - location layout
# London subway stations - Victoria
ot.echarts_Timeline(network2,100,x='lon',y='lat',symbol_size=5,line_width=2, path='../html/network_location_layout_timeline3.html',title='location layout timeline', subtitle='London subway stations',layout='none')









