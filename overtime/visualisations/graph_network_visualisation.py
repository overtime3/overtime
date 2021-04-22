import overtime as ot
from abc import ABC, abstractmethod
import http.server, socketserver, codecs, json

class GraphNetwork_Visualisation(ABC):
    def __init__(self, graph):
        self.graph = graph
        self.node_labels = graph.nodes.labels()
        self.edge_labels = graph.edges.labels()

    @abstractmethod
    def parse_graph_to_json(self):
        pass

    def initialise_server(self):
        PORT = 8000
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f'Serving at port', PORT)
            httpd.serve_forever()

class DiTemporalGraphNetwork_Visualisation(GraphNetwork_Visualisation):
    def __init__(self, graph):
        super().__init__(graph)
        self.start_time = graph.edges.start_times()
        self.end_time = graph.edges.end_times()

    def parse_graph_to_json(self):
        json_dataset = {}
        json_dataset['nodes'] = self.node_labels
        json_dataset['edges'] = []
        for i in range(len(self.node_labels)):
            edge = {}
            source_and_target = self.edge_labels[i].split("-") 
            edge['source'] = source_and_target[0]
            edge['target'] = source_and_target[1]
            edge['start'] = self.start_time[i]
            edge['end'] = self.end_time[i]
            json_dataset['edges'].append(edge)
        return json.dumps(json_dataset)


central = ot.TemporalDiGraph('CentralLine', data=ot.CsvInput('./data/central-inbound.csv'))
visual = DiTemporalGraphNetwork_Visualisation(central)
res = visual.parse_graph_to_json()