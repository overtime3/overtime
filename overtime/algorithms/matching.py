import networkx as nx

def count_matching(TemporalGraph, T, delta):
    """
        A method which returns the time edges in the maximum temporal matching of a temporal graph.
        
        Algorithm 4.1 in the the paper "Computing Maximum Matchings in Temporal Graphs" is implemented below,
        which is available at https://arxiv.org/pdf/1905.05304.pdf.
        
        This is an ∆/(2∆−1)-approximation algorithm for Maximum Temporal Matching.
        
        Parameter(s):
        -------------
        graph : TemporalDiGraph
            A temporal graph.
        root : String
            The label of a node.
        T: int
            Maximum time
        delta: int
            Matching time interval
        Returns:
        --------
        list : time edges in max-matching, the form is as follows
               ('d-c', 7)
    """

    if delta > T:
        raise Exception("Error in input: delta > T")

    delta_template_list = []
    

    """
        The delta_template_list calculation algorithm is implemented by referring to Lemma 24 in the paper.
        
        A ∆-template S is uniquely determined by its leftmost interval. By fixing the leftmost interval of 
        S, the subsequent intervals of S are located in [T] uniformly at distance exactly ∆ − 1 from each other.
    
        The first interval in S is either a partial ∆-window that starts at time slot 1 or a (possibly partial)
        ∆-window that starts in one of the first ∆ time slots of [T].
        
        The following two for loops calculate these two cases respectively.
    """
    
   # Starting from 1, partial delta window with lengths of 1~T-1.
    for first_interval_end in range(1, delta):
        delta_template = []  
        delta_template.append((1,first_interval_end)) 
        temp_end = first_interval_end
        while temp_end+delta <= T:
            temp_start = temp_end+delta
            temp_end = min(T, temp_end+2*delta-1)
            delta_template.append((temp_start, temp_end))
        delta_template_list.append(delta_template)
    
   # delta_template starting from any number in 1~T.
    for first_interval_start in range(1, delta+1):
        delta_template = []
        temp_start = first_interval_start
        temp_end = min(temp_start+delta-1, T)
        delta_template.append((temp_start, temp_end))
        while temp_end+delta <= T:
            temp_start = temp_end+delta
            temp_end = min(T, temp_end+2*delta-1)
            delta_template.append((temp_start, temp_end))
        delta_template_list.append(delta_template)
        
    """
        Algorithm 4.1: ∆/(2∆−1)-Approximation Algorithm (Theorem 23).
        1 M ← ∅. 
        2 for each ∆-template S do
        3   Compute a ∆-temporal matching MS with respect to S. 
        4   if |M^S | > |M| then M ← M^S . 
        5 return M.
    """
    max_cardinality = 0 # Record the current maximum matching cardinality in the for loop of Algorithm 4.1.
    M = [] # Store the temporal edges in the current maximum matching in the for loop of Algorithm 4.1.
    for delta_template in delta_template_list: # Iterate the delta_template list.
        time_edges = [] # Store the temporal edges in the maximum matching of the static graph corresponding to the current delta_template.
        for interval in delta_template:
            subgraph = TemporalGraph.get_temporal_subgraph2(interval) # Calculate the static subgraph in the time interval.
            G = nx.Graph() # Create a graph in networkX.
            for edge in subgraph.edges.aslist(): # Add edges in G from subgraph.
                nodes_of_edge = edge.label.split('-')
                start = edge.start
            
                # Use the start attribute of the edge of the subgraph obtained in the temporal graph as the 
                # time attribute of the edge of the created networkX.Graph().
                G.add_edge(nodes_of_edge[0], nodes_of_edge[1], time = start)
            
            rs = nx.max_weight_matching(G, maxcardinality=False) #Calculate the maximum match in the static graph.
            
            #Return the time attribute of each side in the form of a dictionary, where the key is in the form of 
            #(node1, node2) and the value is in the form of an integer value.
            time = nx.get_edge_attributes(G, 'time') 
            
            """
                Since networkX calculates the maximum matching of undirected graphs, 
                the output edges may be in the opposite order of the nodes of our input edges, 
                so judgment and correction are needed.
            """
            for edge in rs:
                # The case where the node order of the edges in the maximum matching output of networkX is consistent 
                # with the order of our input edges.
                if (edge[0], edge[1]) in time: 
                    time_edges.append((edge[0]+'-'+edge[1] , time[(edge[0], edge[1])]))
                # The case where the node order of the edges in the maximum matching output of networkX is inconsistent 
                # with the order of our input edges.
                else: 
                    time_edges.append((edge[0]+'-'+edge[1] , time[(edge[1], edge[0])]))
        # Determine whether the number of edges in the maximum matching in the current delta_template is the largest.
        if len(time_edges) > max_cardinality: 
            max_cardinality = len(time_edges)
            M = time_edges
            
    return M
    