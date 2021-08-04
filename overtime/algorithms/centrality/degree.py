"""
Temporal degree centrality.
"""


def degree_centrality(graph, labels=None, intervals=None):
    """
        Returns the temporal degree centralities of specified nodes in an undirected temporal graph over a
        time interval.

        Parameter(s):
        -------------
        graph : TemporalGraph
            An undirected temporal graph.
        labels: list
            A list of node labels to calculate centralities for. Default is all nodes in the temporal graph.
            Example: ["A", "B", "C", ...]
        intervals : tuple/List
            A tuple of intervals (pairs of start and end times) for the temporal graph to be restricted to.
            Example: ((0,3), (5,7))

        Returns:
        --------
        temporal_degree : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B:1.2, C:2.5, ...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            degree_centrality = degree_centrality(graph, labels=["A", "B", "C"], intervals=((1, 5), (8, 10)))

        See also:
        ---------
            calculate_reachability

    """
    # Restrict graph to specified time interval
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)

    # Only calculate for specified labels
    if not labels:
        labels = graph.nodes.labels()   # If labels not specified, set labels to all nodes in input graph

    # Initialize
    node_count = {label: 0 for label in labels}

    # Calculate total degree for each node
    for edge in graph.edges.aslist():       # Increment temporal degree every time node is seen as endpoint of edge

        node_count[edge.node1.label] += 1
        node_count[edge.node2.label] += 1

    # Normalize by size of graph
    normalization_factor = graph.nodes.count() - 1
    temporal_degree = {label: value / normalization_factor for label, value in node_count.items()}

    # Sort by descending centrality value
    sorted_temporal_degree = {label: value for label, value in sorted(temporal_degree.items(),
                                                                      key=lambda item: item[1],
                                                                      reverse=True)}

    return sorted_temporal_degree
