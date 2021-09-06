"""
Algorithms for computing closeness centrality from temporal graph objects.
"""

from overtime.algorithms.paths.optimality import *
from overtime.algorithms.additional_tools import convert_to_directed


def temporal_closeness(graph, optimality="fastest", labels=None, intervals=None, normalize=False, cent_evo=False, add_data=False):
    """
        Returns the closeness centralities of nodes in a temporal graph.

        Parameter(s):
        -------------
        graph : TemporalGraph
            A directed or undirected temporal graph.
        optimality : string
            Concept of optimal path in a temporal graph to be used. Can be "fastest" or "shortest".
        labels: list
            A list of node labels. Default is all nodes in input graph.
        intervals : tuple/List
            A tuple of intervals (start & end time pairs). Default is the interval
            the graph is defined over.
            For example: ((0,3), (5,7)).
        cent_evo : bool
            Enable centrality evolution. Returns centrality values at each snapshot/ timestep, rather than a centrality
            value for the whole lifetime of the graph.
        add_data : bool
            Whether to add the centrality values to the data attributes of the nodes in the nodes collection.

        Returns:
        --------
        closeness_centrality : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B: 1.2, C: 2.5...}
            If centrality evolution is enabled, returns a dict where values are lists of the centrality values at each
            snapshot/ timestep.
            For example: {A: [1.1, 3.2, 4.1], B: [1.5, 2.3, 4.5]...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            closeness_values = closeness_centrality(graph, optimality="fastest", labels=["A", "B", ...], intervals=((1, 5), (8, 10)))

        Notes:
        ------
        This implementation for calculating temporal closeness centralities utilizes an algorithm for calculating
        fastest/ shortest path durations/ lengths outlined in "Path Problems in Temporal Graphs" (Wu et al. 2014), found here:
        https://www.vldb.org/pvldb/vol7/p721-wu.pdf. Our algorithm takes as input a temporal graph (rather than, say, a
        static expansion) and returns the temporal closeness centrality of all nodes in the graph- that is, the normalized
        sum of reciprocal distances from each node to all other nodes. Temporal closeness centrality can be based on
        multiple notions of optimal path, and as such this algorithm can be executed using either the "shortest" or "fastest"
        notions of optimal path as outlined in Buß et al. (2020). Normalization is applied as seen in "Temporal Node
        Centrality in Complex Networks" (Kim and Anderson, 2011), found here:
        https://www.cl.cam.ac.uk/~rja14/Papers/TemporalCentrality.pdf.

        See also:
        ---------
        calculate_fastest_path_durations

    """
    # If input graph is undirected, convert to bidirectional graph
    if not graph.directed:
        graph = convert_to_directed(graph)

    # Restrict graph to specified time interval
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)

    # Only calculate for specified labels
    if not labels:
        labels = graph.nodes.labels()  # if labels not specified, set to all nodes in input graph

    # Initialize
    closeness_centrality = {label: [] for label in labels}  # initialize dictionary to store node : closeness centrality

    # Iterate over [t, j] such that graph.edges.start() <= t <= graph.edges.end() -- for centrality evolution
    for t in range(graph.edges.start(), graph.edges.end()):

        # Iterate over nodes
        for label in graph.nodes.labels():

            # Calculate optimal path magnitude from current node to all other nodes
            path_magnitudes = None
            if optimality == "fastest":
                path_magnitudes = [*calculate_fastest_path_durations(graph, interval=(t, graph.edges.end()), root=label).values()]
            elif optimality == "shortest":
                path_magnitudes = [*calculate_shortest_path_lengths(graph, interval=(t, graph.edges.end()), root=label).values()]

            # Take reciprocal of all magnitudes and sum
            path_magnitudes_reciprocal = [1 / value for value in path_magnitudes if value != 0]
            sum_path_magnitudes_reciprocal = sum(path_magnitudes_reciprocal)

            # If centrality evolution enabled, append a value for each snapshot/ timepoint
            if cent_evo:
                closeness_centrality[label].append(sum_path_magnitudes_reciprocal)
            # If centrality evolution disabled, take centrality over first full interval and stop
            else:
                closeness_centrality[label] = sum_path_magnitudes_reciprocal

        if not cent_evo:
            break

    # Apply normalization
    if normalize:
        normalization_factor = (graph.nodes.count() - 1) * (graph.edges.end() - graph.edges.start())
        # If centrality evolution enabled
        if cent_evo:
            closeness_centrality = {key: [v / normalization_factor for v in value] for key, value in closeness_centrality.items()}
        # If centrality evolution not enabled
        else:
            closeness_centrality = {label: value / normalization_factor for label, value in closeness_centrality.items()}

    # Add data to nodes
    if add_data:
        for node in graph.nodes.set:
            node.data["closeness"] = closeness_centrality[node.label]

    return closeness_centrality
