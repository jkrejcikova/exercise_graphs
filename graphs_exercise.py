import matplotlib.pyplot as plt
import pandas as pd


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
def dfs(graph, start):
    # Keep track of visited vertices and the order they are visited
    visited = set()
    order = []

    def _visit(vertex):
        visited.add(vertex)
        order.append(vertex)

        # Sort neighbours alphabetically to resolve ties deterministically
        for neighbour in sorted(graph.get(vertex, [])):
            if neighbour not in visited:
                _visit(neighbour)

    # If the start vertex exists in the graph, begin DFS
    if start in graph:
        _visit(start)

    return order


def connected_components(graph):
    components = []
    seen = set()

    # Find connected components by calling DFS on unvisited vertices
    for vertex in graph:
        if vertex not in seen:
            reachable = dfs(graph, vertex)
            component = set(reachable)
            components.append(component)
            seen.update(component)

    return components


def is_weakly_connected(graph):
    # An empty graph or single isolated vertex is considered weakly connected
    if len(graph) <= 1:
        return True

    # 1. Build the undirected shadow graph
    shadow = {}
    for vertex in graph:
        shadow[vertex] = []

    for u, neighbours in graph.items():
        for v in neighbours:
            shadow.setdefault(u, [])
            shadow.setdefault(v, [])
            shadow[u].append(v)
            shadow[v].append(u)

    # 2. Check if the undirected shadow forms exactly one component
    components = connected_components(shadow)
    return len(components) == 1

# TASK 4

def eulerian_type(graph, directed=False):
    # Handle the undirected case
    if not directed:
        # Check connectivity: an undirected graph must have exactly one component
        components = connected_components(graph)
        if len(components) != 1:
            return "none"

        deg = degrees(graph)
        odd_count = 0
        for d in deg.values():
            if d % 2 != 0:
                odd_count += 1

        if odd_count == 0:
            return "circuit"
        elif odd_count == 2:
            return "path"
        else:
            return "none"

    # Handle the directed case
    else:
        # Check weak connectivity
        if not is_weakly_connected(graph):
            return "none"

        in_deg, out_deg = in_out_degree(graph)
        start_nodes = 0  # out - in == +1
        end_nodes = 0    # in - out == +1

        for v in graph:
            diff = out_deg[v] - in_deg[v]
            if diff == 0:
                continue
            elif diff == 1:
                start_nodes += 1
            elif diff == -1:
                end_nodes += 1
            else:
                # Any diff other than 0, +1, -1 immediately breaks Eulerian conditions
                return "none"

        if start_nodes == 0 and end_nodes == 0:
            return "circuit"
        elif start_nodes == 1 and end_nodes == 1:
            return "path"
        else:
            return "none"


# TASK 3: G1 (undirected)
# G1 (undirected)
g1_edges = [
    ("A", "D"), ("A", "I"), ("B", "D"), ("B", "F"), ("B", "G"), ("B", "I"),
    ("C", "E"), ("C", "H"), ("C", "J"), ("C", "K"), ("D", "F"), ("D", "G"),
    ("E", "J"), ("H", "J"), ("J", "K")
]
g1 = build_adjacency_list(g1_edges, directed=False)
print("G1 DFS from A:", dfs(g1, "A"))  # ['A', 'D', 'B', 'F', 'G', 'I']
print("G1 DFS from C:", dfs(g1, "C"))  # ['C', 'E', 'J', 'H', 'K']
print("G1 Components:", connected_components(g1))

# G2 (directed)
g2_edges = [("P", "Q"), ("Q", "R"), ("R", "P"), ("R", "S"), ("T", "S")]
g2 = build_adjacency_list(g2_edges, directed=True)
print("G2 DFS from P:", dfs(g2, "P"))  # ['P', 'Q', 'R', 'S']
print("G2 DFS from S:", dfs(g2, "S"))  # ['S']
print("G2 DFS from T:", dfs(g2, "T"))  # ['T', 'S']
print("G2 Weakly Connected:", is_weakly_connected(g2))  # True

# TASK 4
# 1. G1 (undirected) -> none (disconnected)
print("G1:         ", eulerian_type(g1, directed=False))

# 2. G3 (undirected)
g3_edges = [
    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
    ("D", "E"), ("E", "F"), ("F", "G"), ("G", "D")
]
g3 = build_adjacency_list(g3_edges, directed=False)
print("G3:         ", eulerian_type(g3, directed=False))  # circuit

# 3. G4 (undirected): G3 without edge {F, G}
g4_edges = [
    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
    ("D", "E"), ("E", "F"), ("G", "D")
]
g4 = build_adjacency_list(g4_edges, directed=False)
print("G4:         ", eulerian_type(g4, directed=False))  # path

# 4. G5a (directed)
g5a_edges = [("1", "2"), ("2", "3"), ("3", "1"), ("1", "4"), ("4", "1")]
g5a = build_adjacency_list(g5a_edges, directed=True)
print("G5a:        ", eulerian_type(g5a, directed=True))   # circuit

# 5. G5b (directed): G5a without edge (4, 1)
g5b_edges = [("1", "2"), ("2", "3"), ("3", "1"), ("1", "4")]
g5b = build_adjacency_list(g5b_edges, directed=True)
print("G5b:        ", eulerian_type(g5b, directed=True))   # path

# 6. Königsberg bridges (undirected multigraph with 7 edges)
koenigsberg_edges = [
    ("A", "B"), ("A", "B"),
    ("A", "C"), ("A", "C"),
    ("A", "D"),
    ("B", "D"),
    ("C", "D")
]
koenigsberg = build_adjacency_list(koenigsberg_edges, directed=False)
print("Königsberg: ", eulerian_type(koenigsberg, directed=False))  # none