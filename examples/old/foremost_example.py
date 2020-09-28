from inputs.classes import CsvInput
from components.graphs import TemporalGraph

input_data = CsvInput('./network.csv')

graph = TemporalGraph('TestNetwork')
graph.build(input_data)


# calculate foremost time (to be added)
foremost = {}
a = graph.nodes.get('a')
start = graph.edges.start()
end = graph.edges.end()

for node in graph.nodes.set:
    foremost[node.label] = {}
    foremost[node.label]['time'] = float('inf')
    foremost[node.label]['source'] = ''

foremost[a.label]['time'] = start
foremost[a.label]['source'] = a.label

for edge in graph.edges.set:
    if edge.start + edge.duration <=end and edge.start >= foremost[edge.source.label]['time']:
        if edge.start + edge.duration < foremost[edge.sink.label]['time']:
            foremost[edge.sink.label]['time'] = edge.start + edge.duration
            foremost[edge.sink.label]['source'] = edge.source.label
    elif edge.start >= end:
        break

for node, info in foremost.items():
    print("{} | {},{}".format(node, info['time'], info['source']))
