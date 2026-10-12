
# TASK 1

vertices = {'P1', 'P2', 'P3', 'P4', 'P5'}
edges = [('P1', 'P2'), ('P1', 'P3'), ('P2', 'P3'), ('P3', 'P4'), ('P4', 'P5')]

def build_adjacency_list(edges, directed=False):
    graph = {}

    for u,v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []

    for u,v in edges:
        if directed==False:
            graph[v].append(u)
            graph[u].append(v)
        if directed==True:
            graph[u].append(v)

    return graph

def degrees(graph):
    result = {}

    for vertex, neighbours in graph.items():
        deg = len(neighbours)
        result[vertex] = deg

    return result

def in_out_degree(graph):
    out_degree = {}
    for vertex, neighbours in graph.items():
        out_degree[vertex] = len(neighbours)

    in_degree = {}
    for vertex in graph:
        in_degree[vertex] = 0

    for neighbours in graph.values():
        for target in neighbours:
            in_degree[target] += 1

    return in_degree, out_degree

our_graph = build_adjacency_list(edges, directed=False)
print(our_graph)

our_degrees = degrees(our_graph)
print(our_degrees)

# The in-degree sum always equals the out-degree sum.
# Can a directed graph have exactly one vertex with deg⁻(v) ≠ deg⁺(v)? Exactly three? Why, or why not?
#   1. Exactly one: NO. Because sum(in_degree) == sum(out_degree), the sum of
#      (in_degree - out_degree) across all vertices must be 0.
#   2.  Exactly three: YES. Non-zero differences can cancel each other out.


# TASK 3

