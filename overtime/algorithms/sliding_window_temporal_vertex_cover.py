import overtime as ot
import copy
import itertools


# Give a vertex set and return all subsets
def getSubSet(vertexSet):
    N = len(vertexSet)
    subSet = []

    for i in range(2 ** N):
        combo = []
        for j in range(N):
            if (i >> j) % 2:
                combo.append(vertexSet[j])
        subSet.append(combo)
    return subSet


# Find all possible combinations of A1, A2, ... ,A_delta
def delta_A_union(subset, delta):
    u_set = []
    b = [subset] * delta
    c = list(itertools.product(*b))
    for j in c:
        s = {}
        for i in range(1, delta + 1):
            s.update({i: j[i - 1]})
        u_set.append(s)
    return u_set


# Check whether a combination of A_1,...A_delta is the vertex cover set of temporal graph
# Returns True if it is vertex cover set of temporal graph
def check_is_vertex_cover(temporalgraph, unionset):
    graph = copy.deepcopy(temporalgraph)
    for i in unionset.values():
        for j in i:
            graph.remove_node(j)

    if graph.edges.labels() == []:
        return True
    else:
        return False


# Find the minimum cardinality vertex cover set in a big set which contain all of vertex cover set
# and return this set and the minimum cardinality
def get_min_cardinality(vc_set):
    # Calculate the length of each A_1...A_delta and save it to the dictionary count
    count = {}
    for i in range(len(vc_set)):
        c = []
        for j in vc_set[i].values():
            c.append(len(j))
        count.update({i: c})

    # Find the position of the item with the smallest value in the dictionary count,
    # and then find the A_1... A_delta of the smallest cardinality at the same position in vc_set
    min_key_value = min(count.items(), key=lambda x: x[1])
    min_c = 0
    for i in min_key_value[1]:
        min_c = min_c + i
    min_set = vc_set[min_key_value[0]]
    return min_c, min_set


# Vertex covering algorithm for static graphs
def vertex_cover(staticGraph):
    # Find all vertex subsets of the static graph
    subSet = getSubSet(staticGraph.nodes.labels())

    vertexCover = []
    # Judge whether each subset is the vertex cover set of this static graph
    for s in subSet:
        graph = copy.deepcopy(staticGraph)
        # Remove the vertices in the subset from the static graph
        for node in s:
            graph.remove_node(node)
        # When the first vertex cover set is found,
        # the minimum vertex cover set is found and return this subset
        if graph.edges.labels() == []:
            vertexCover.append(s)
    # Sort all vertex cover sets
    vertexCover.sort(key=len)
    # Returns the smallest vertex cover set
    return vertexCover[0]


# Main algorithm
def SW_TVC(temporalGraph, delta):
    # Initialize the swtvc set and F function of smallest cardinality swtvc
    swtvc = {}
    f_t_A = {}
    lifeTime = len(temporalGraph.edges.timespan())

    # When delta = 1, it becomes a 1-tvc problem.
    # Find the minimum vertex coverage of each time slot and get the minimum cardinality
    if delta == 1:

        # Find the minimum vertex coverage of each time slot
        for t in temporalGraph.edges.timespan():
            subGraph = temporalGraph.get_snapshot(t)
            swtvc.update({t: vertex_cover(subGraph)})

        # Get the minimum cardinality
        min_ca = 0
        for t, i in swtvc.items():
            min_ca = min_ca + len(i)
            f_t_A.update({t: min_ca})

    # When 1< delta <= lifeTime, execute main algorithm
    elif 1 < delta <= lifeTime:

        # Firstly, find all vertex subsets of temporal graph vertices
        subSet = getSubSet(temporalGraph.nodes.labels())

        # Then initialize list is used to store the all vertex cover set for each sliding window
        vertex_cover_set = [[]] * (lifeTime - delta + 2)

        # In each sliding window
        for t in range(1, lifeTime - delta + 2):
            # Iterate over all possible combinations of A_1,...,A_delta
            for unionA in delta_A_union(subSet, delta):
                subgraph = temporalGraph.get_temporal_subgraph((t, t + delta - 1))

                # Find all vertex cover combinations in G[t,t+delta-1]
                if check_is_vertex_cover(subgraph, unionA):
                    vertex_cover_set[t].append(unionA)

            # If there is a vertex cover set
            if vertex_cover_set[t] != []:

                # If it is the first sliding window,
                # the minimum cardinality is the cardinality of the current minimum vertex cover set
                if t == 1:
                    min_vc = get_min_cardinality(vertex_cover_set[t])
                    min_cardinality = min_vc[0]
                    min_vertex_cover = min_vc[1]
                    f_t_A.update({t: min_cardinality})
                    swtvc = min_vertex_cover
                # If it is not the first sliding window
                else:
                    # Find all vertex covering combinations which make A1...A_delta-1 equal to A2...A_delta of
                    # the previous window, then find the minimum combination that fit the conditions
                    temp = vertex_cover_set[t]
                    for i in range(len(temp) - 1, -1, -1):
                        for j in range(1, delta):
                            if temp[i][j] != swtvc[j + t - 1]:
                                del temp[i]
                    min_vc = get_min_cardinality(temp)
                    min_vertex_cover = min_vc[1]

                    # Get A_delta from the minimum combination which found by last step
                    delta_A = min_vertex_cover[delta]
                    f_t_A.update({t: f_t_A[t - 1] + len(delta_A)})
                    swtvc.update({t + delta - 1: delta_A})
            # If there is no Vertex overlay set, the minimum cardinality is infinite
            else:
                f_t_A.update({t: -1})
    else:

        print("Error! delta must in [1,{}]".format(len(temporalGraph.edges.timespan())))

    return f_t_A, swtvc


# Get all temporalgraphs with only one edge e = uv
def get_temporalgraphs_with_single_edge(temporalGraph):
    # Create a list to store all the single_edge graphs
    singleEdgeGraphs = []

    # Get the underlying graph of temporal graph
    a = temporalGraph.get_underlying_graph()

    # for each edge of the underlying graph, create temporal graph only containing this edge
    for edge in a.edges.ulabels():

        # Get all uid of this edge
        edgeUid = temporalGraph.edges.get_edge_by_label(edge).uids()

        # Copy the original temporal graph and delete all edges that do not match these UIDs
        seg = copy.deepcopy(temporalGraph)
        for everyEdge in seg.edges.uids():
            if everyEdge not in edgeUid:
                seg.remove_edge(everyEdge)

        # Add the temporal graph with single edge to the list
        singleEdgeGraphs.append(seg)

    return singleEdgeGraphs


# SW-TVC on single-edge temporal graphs.
def single_edge_swtvc(temporalgraph, delta, lifeTime):
    # Initialize vertex cover set S and t
    S = []
    t = 1

    while t <= lifeTime - delta + 1:

        # use 'max_ R' to record the maximum r,
        # and use 'exist' to mark whether there are edges in this sliding window
        exist = 0
        max_r = 0

        # Check whether there is an edge at each time slot of each sliding window
        for r in range(t, t + delta):

            # If there exist edge, record exist as 1 and find the largest r
            if temporalgraph.get_snapshot(r).edges.labels() != []:
                exist = 1
                max_r = r

        if exist == 1:
            # If there exist edge, store one of vertex in this edge and max_r to set S
            S.append([temporalgraph.get_snapshot(max_r).edges.labels()[0][0], max_r])
            t = max_r + 1
        else:
            t = t + 1

    return S


def d_approximation_swtvc(temporalgraph, delta):
    lifeTime = len(temporalgraph.edges.timespan())

    # Initialize vertex cover set s
    S = {}
    for i in range(1, lifeTime + 1):
        S.update({i: []})

    # Find the single edge subgraph of temporal graph
    single_edge_temporalgraph = get_temporalgraphs_with_single_edge(temporalgraph)

    # Run 'single_edge_swtvc' algorithm for each single edge subgraph
    for singleEdge in single_edge_temporalgraph:
        Se = single_edge_swtvc(singleEdge, delta, lifeTime)
        print(Se)
        # Merge all results of single edge temporal graph into the final vertex cover set S
        for vertex in Se:
            if vertex[0] not in S[vertex[1]]:
                S[vertex[1]].append(vertex[0])
    return S
