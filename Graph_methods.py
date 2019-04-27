from networkx import *


def get_subgraph(graph, nodes):
    return subgraph(graph.Graph, nodes)


def parse_graph_from_gexf(path):
    return read_gexf(path)


def dfs(gr, start):
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(set(neighbors(gr, vertex)) - visited)
    return visited


def ordered_dfs(gr, start, order, marked):

    marked.add(start)
    for v in neighbors(gr,start):
        if v not in marked:
            ordered_dfs(gr,v,order,marked)
    order.append(start)

def dfs_by_order(gr, start, marked,component):
    marked.add(start)
    component.append(start)
    for v in neighbors(gr, start):
        if v not in marked:
            dfs_by_order(gr, start, marked, component)

class GraphClass:

    def __init__(self, path):
        self.Graph = parse_graph_from_gexf(path)

    def get_weak_connectivity(self):
        weak_components = []
        for node in self.Graph.nodes:
            if not any(node in component for component in weak_components):
                weak_components.append(dfs(self.Graph, node))
        return weak_components

    def get_strong_connectivity(self):
        order = []
        marked = set()
        strong_components = []
        for node in reverse(self.Graph, True):
            if node not in marked:
                ordered_dfs(self.Graph, node, order, marked)
        for v in list(reversed(order)):
            component = dfs(self.Graph, v)
            if component not in strong_components:
                strong_components.append(component)
        return strong_components








    def nodes(self):
        return self.Graph.nodes

    def degree(self, node):
        return degree(self.Graph, node)

