from overtime.algorithms.paths import *


def closeness_centrality(graph, optimality=None, labels=None, intervals=None):
    """
        Returns the closeness centralities of specified nodes in a temporal graph over a
        time interval.

        Parameter(s):
        -------------
        graph : TemporalGraph
            An undirected temporal graph.
        labels: list
            A list of node labels. Default is all nodes in input graph.
        intervals : tuple/List
            A tuple of intervals (start & end time pairs). Default is the interval
            the graph is defined over.
            For example: ((0,3), (5,7)).
        optimality : string
            Concept of optimal path in a temporal graph to be used. Can be "fastest" or "shortest".

        Returns:
        --------
        closeness_centrality : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B:1.2, C:2.5...}

        TODO
        ----
        Allow user to select optimality --> requires implementing Wu et al. SHORTEST temporal paths algorithm

    """
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)  # restrict graph to specified time interval

    if not labels:
        labels = graph.nodes.labels()  # if labels not specified, set to all nodes in input graph

    closeness_centrality = {label: 0 for label in
                              labels}  # initialize dictionary to store node : closeness centrality

    for label in graph.nodes.labels():
        fastest_path_durations = [*calculate_fastest_path_durations(graph, root=label).values()]

        fastest_path_durations_reciprocal = [1 / value for value in fastest_path_durations if value != 0]

        sum_reciprocal_distances = sum(fastest_path_durations_reciprocal)

        closeness_centrality[label] = sum_reciprocal_distances

    # TODO: apply normalization

    return closeness_centrality
