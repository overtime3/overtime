def betweenness_centrality(graph, optimality="shortest", intervals=None):
    """
        Returns the betweenness centralities of specified nodes in a temporal graph over a
        time interval.

        Parameter(s):
        -------------
        graph : TemporalGraph
            An undirected temporal graph.
        intervals : tuple/List
            A tuple of intervals (start & end time pairs). Default is the interval
            the graph is defined over.
            For example: ((0,3), (5,7)).
        optimality : string
            Concept of optimal path in a temporal graph to be used. Can be "shortest" or "foremost".

        Returns:
        --------
        betweeness_centrality : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B:1.2, C:2.5...}

        TODO
        ----
        Allow user to select optimality --> requires implementing Wu et al. SHORTEST temporal paths algorithm

    """
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)  # restrict graph to specified time interval

    shortest_centrality = {node: 0 for node in graph.nodes.labels()}
    foremost_centrality = {node: 0 for node in graph.nodes.labels()}

    for s in graph.nodes.labels():

        # Initialize for nodes
        dist_v = {node: -1 for node in graph.nodes.labels()}
        sigma_v = {node: 0 for node in graph.nodes.labels()}
        t_min_v = {node: -1 for node in graph.nodes.labels()}

        # Initialize for node appearances
        node_appearances = [(node, t) for node in graph.nodes.labels() for t in range(graph.edges.end())]

        delta_v_t_shortest = {v_t: 0 for v_t in node_appearances}
        delta_v_t_foremost = {v_t: 0 for v_t in node_appearances}
        sigma_v_t = {v_t: 0 for v_t in node_appearances}
        paths_v_t = {v_t: [] for v_t in node_appearances}
        dist_v_t = {v_t: -1 for v_t in node_appearances}

        # Initialize values for current source node
        dist_v[s] = 0
        dist_v_t[(s, 0)] = 0
        t_min_v[s] = 0
        sigma_v[s] = 1
        sigma_v_t[(s, 0)] = 1

        # Initialize stack and queue
        S = []          # LIFO -- Stack
        Q = [(s, 0)]    # FIFO -- Queue

        while Q:

            v, t = Q.pop(0)

            # Iterate over temporal neighbours
            for w, t_ in [neighbour for neighbour in graph.nodes.get(v).temporal_neighbours() if t <= neighbour[1]]:

                # For first visit to (w, t_)
                if dist_v_t[(w, t_)] == -1:
                    dist_v_t[(w, t_)] = dist_v_t[(v, t)] + 1
                    if dist_v[w] == -1:       # Shortest path to w
                        dist_v[w] = dist_v_t[(v, t)] + 1

                    S.append((w, t_))
                    Q.append((w, t_))

                if dist_v_t[(w, t_)] == dist_v_t[(v, t)] + 1:
                    sigma_v_t[(w, t_)] += sigma_v_t[(v, t)]
                    paths_v_t[(w, t_)].append((v, t))
                    if dist_v_t[(w, t_)] == dist_v[w]:
                        sigma_v[w] += sigma_v_t[(v, t)]

                if t_min_v[w] == -1 or t_ < t_min_v[w]:
                    t_min_v[w] = t_


        shortest_centrality[s] = shortest_centrality[s] - len([i for i in dist_v.values() if i >= 0]) + 1
        foremost_centrality[s] = foremost_centrality[s] - len([i for i in dist_v.values() if i >= 0]) + 1

        while S:

            w, t_ = S.pop(-1)

            if dist_v_t[(w, t_)] == dist_v[w]:
                delta_v_t_shortest[(w, t_)] += (sigma_v_t[(w, t_)] / sigma_v[w])

            if t_ == t_min_v[w]:
                delta_v_t_foremost[(w, t_)] += 1

            for v, t in paths_v_t[(w, t_)]:

                delta_v_t_shortest[(v, t)] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_shortest[(w, t_)]
                shortest_centrality[v] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_shortest[(w, t_)]

                delta_v_t_foremost[(v, t)] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_foremost[(w, t_)]
                foremost_centrality[v] += (sigma_v_t[(v, t)] / sigma_v_t[(w, t_)]) * delta_v_t_foremost[(w, t_)]

    if optimality == "shortest":
        return shortest_centrality

    elif optimality == "foremost":
        return foremost_centrality
