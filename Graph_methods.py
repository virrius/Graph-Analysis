from networkx import *

def get_max_connectivity_component(graph, nodes):
    return subgraph(graph.Graph,nodes)

def parse_graph_from_gexf(path):
    return read_gexf(path)


def dfs(graph_mat, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph_mat[vertex] - visited)
    return visited


class GraphClass:

    def __init__(self, path):
        self.Graph = parse_graph_from_gexf(path)

    def get_weak_connectivity(self):
        return weakly_connected_components(self.Graph)

    def get_strong_connectivity(self):
        return strongly_connected_components(self.Graph)

    def nodes(self):
        return self.Graph.nodes

    def degree(self, node):
        return degree(self.Graph, node)

