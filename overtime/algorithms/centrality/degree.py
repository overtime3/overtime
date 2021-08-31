"""
Algorithms for computing temporal degree centrality for temporal graph objects.
"""


def temporal_degree(graph, labels=None, intervals=None, in_out=None, add_data=False):
    """
        Returns the temporal degree centralities of nodes in a temporal graph.

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
        in_out : string
            What type of degree centrality to use. Can be "in" for in-degree, "out" for out-degree. Leave unspecified
            for undirected graphs where normal degree centrality is default.
        normalize : bool
            Whether to apply normalization to the produced centrality values.

        Returns:
        --------
        temporal_degree : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B:1.2, C:2.5, ...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            degree_values = degree_centrality(graph, labels=["A", "B", "C"], intervals=((1, 5), (8, 10)))

        Notes:
        ------
        Here, temporal degree centrality is the average of a nodes' degree over the snapshots of the graph in a given
        time interval. Degree may refer to in-degree, out-degree, or both.

    """
    if not graph.directed and in_out == "in" or not graph.directed and in_out == "out":
        raise TypeError("Graph must be directed for in- or out- degree.")
    if graph.directed and in_out is None:
        raise TypeError("If input graph is directed, in- or out- degree must be specified.")

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

        if not graph.directed:                          # Undirected graph - normal degree centrality
            node_count[edge.node1.label] += 1
            node_count[edge.node2.label] += 1

        if graph.directed and in_out == "in":           # Directed graph - in-degree
            node_count[edge.node2.label] += 1

        if graph.directed and in_out == "out":          # Directed graph - out-degree
            node_count[edge.node1.label] += 1

    # Calculate average over snapshots
    graph_age = graph.edges.end() - graph.edges.start()
    temporal_degree_centrality = {label: value / graph_age for label, value in node_count.items()}

    # Add data to nodes
    if add_data:
        for node in graph.nodes.set:
            node.data["degree"] = temporal_degree_centrality[node.label]

    return temporal_degree_centrality
