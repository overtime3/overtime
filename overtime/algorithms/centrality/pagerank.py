"""
Algorithms for computing temporal PageRank scores from temporal graph objects
"""


def temporal_pagerank(graph, alpha=0.85, beta=0.5, t=None, intervals=None):
    """
        Returns the temporal PageRank score of nodes in a directed temporal graph.

        Parameter(s):
        -------------
        graph : TemporalDiGraph
            An directed temporal graph.
        alpha : float
            Probability of intitiating new walk from current node.
        beta : float (0, 1]
            Transition probability.
        intervals : tuple/List
            A tuple of intervals (pairs of start and end times) for the temporal graph to be restricted to.
            Example: ((0,3), (5,7))

        Returns:
        --------
        pagerank : dict
            The PageRank score of each node.
            For example: {A: 0.15, B: 0.19, C: 1.41, ...}

        Notes:
        ------

    """

    if t is None:
        t = graph.edges.end()

    # Initialize
    pagerank = {node: 0 for node in graph.nodes.labels()}
    active_walks = {node: 0 for node in graph.nodes.labels()}

    # Iterate over edge stream
    for edge in graph.edges.set:

        if edge.start > t:
            break

        u = edge.node1.label
        v = edge.node2.label

        pagerank[u] += (1 - alpha)
        active_walks[u] += (1 - alpha)
        pagerank[v] += active_walks[u] * alpha

        if 0 < beta < 1:
            active_walks[v] += active_walks[u] * (1 - beta) * alpha
            active_walks[u] *= beta

        elif beta == 1:
            active_walks[v] += active_walks[u] * alpha
            active_walks[u] = 0

    return pagerank