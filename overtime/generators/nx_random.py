
import networkx as nx
from overtime.generators.classes import Generator



class RandomGNP(Generator):
    """
        A random GNP graph with n nodes where each edge is created with a possibility p.
        Generated using the networkx gnp_random_graph static generator at each timestep.

        Parameter(s):
        -------------
        n : Integer
            Number of nodes.
        p : Float
            Probability of edge creation.
        directed : Boolean
            Switch to control whether the created graph is directed.
        start : Integer
            Start time of temporal timespan.
        end : Integer
            End time of temporal timespan.

        Object Propertie(s):
        --------------------
        data : Dict
            Inherited from Generator.

        Example(s):
        -----------
            gnp_data = RandomGNP(40, 0.2, start=1, end=20)
            graph = TemporalGraph('random_gnp_network', data=gnp_data)

        See also:
        ---------
            Generator
    """

    def __init__(self, n=10, p=0.5, directed=False, start=0, end=10):
        super().__init__()
        self.generate(n, p, directed, start, end)


    def generate(self, n, p, directed, start, end):
        ne, nn = 0, 0 # initialize counters
        # for timestep in specified timespan.
        for t in range(start, end+1):
            # generate a static graph at time t.
            static = nx.gnp_random_graph(n, p, directed=directed)
            # for each static edge, add a temporal edge at time t to data.
            for edge in static.edges:
                # add edge data, conforming to data naming convention.
                self.data['edges'][ne] = {
                    'node1': edge[0],
                    'node2': edge[1],
                    'tstart': t,
                    'tend': None,
                }
                ne += 1

            # at the first timestep, add all the nodes to data
            # (all nodes are created in first static graph).
            if t == start:
                for node in static.nodes:
                    self.data['nodes'][nn] = node
                    nn += 1
