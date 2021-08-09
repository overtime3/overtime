"""
Algorithms for computing closeness centrality from temporal graph objects.
"""

from overtime.algorithms.paths.paths import calculate_fastest_path_durations


def temporal_closeness_centrality(graph, optimality="fastest", labels=None, intervals=None):
    """
        Returns the closeness centralities of nodes in a temporal graph.

        Parameter(s):
        -------------
        graph : TemporalGraph
            An undirected temporal graph.
        optimality : string
            Concept of optimal path in a temporal graph to be used. Can be "fastest" or "shortest".
        labels: list
            A list of node labels. Default is all nodes in input graph.
        intervals : tuple/List
            A tuple of intervals (start & end time pairs). Default is the interval
            the graph is defined over.
            For example: ((0,3), (5,7)).


        Returns:
        --------
        closeness_centrality : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B: 1.2, C: 2.5...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            closeness_values = closeness_centrality(graph, optimality="fastest", labels=["A", "B", ...], intervals=((1, 5), (8, 10)))

        Notes:
        ------
        This implementation for calculating fastest temporal path durations utilizes an algorithm for calculating
        fastest path durations outlined in "Path Problems in Temporal Graphs" (Wu et al. 2014), found here:
        https://www.vldb.org/pvldb/vol7/p721-wu.pdf. Our algorithm takes as input a temporal graph (rather than, say, a
        static expansion) and returns the temporal closeness centrality of all nodes in the graph- that is, the normalized
        sum of reciprocal distances from each node to all other nodes. Temporal closeness centrality can be based on multiple
        notions of optimal path, and as such this algorithm can be executed using either the "shortest" or "fastest"
        notions of optimal path as outlined in Buß et al. (2020). Normalization is applied as seen in "Temporal Node
        Centrality in Complex Networks" (Kim and Anderson, 2011), found here:
        https://www.cl.cam.ac.uk/~rja14/Papers/TemporalCentrality.pdf.

        See also:
        ---------
        calculate_fastest_path_durations

        TODO
        ----
        - Allow user to select optimality
            --> Implement Wu et al. *shortest* paths algorithm
        - Everything in the betweenness centrality to-do

    """
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)  # restrict graph to specified time interval

    if not labels:
        labels = graph.nodes.labels()  # if labels not specified, set to all nodes in input graph

    closeness_centrality = {label: 0 for label in labels}  # initialize dictionary to store node : closeness centrality

    for label in graph.nodes.labels():

        fastest_path_durations = [*calculate_fastest_path_durations(graph, root=label).values()]

        fastest_path_durations_reciprocal = [1 / value for value in fastest_path_durations if value != 0]

        sum_reciprocal_distances = sum(fastest_path_durations_reciprocal)

        closeness_centrality[label] = sum_reciprocal_distances

    # TODO: apply normalization

    return closeness_centrality
