from networkx import *
from collections import deque
from collections import defaultdict

def get_undirected_subgraph(graph, nodes):
    return subgraph(graph.Graph.to_undirected(), nodes)


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


def paths_bfs(gr, start):
    visited = set()
    paths = defaultdict(lambda: 0)
    queue = deque()
    queue.append(start)
    layer_queue = deque()
    path_length = 0

    while queue or layer_queue:
        if not queue:
            queue.extend(list(layer_queue))
            layer_queue.clear()
            path_length += 1
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            layer_queue.extend(set(neighbors(gr, vertex)) - visited)
            paths[vertex] = path_length
    return paths


def ordered_dfs(gr, start, order, marked):

    marked.add(start)
    for v in neighbors(gr, start):
        if v not in marked:
            ordered_dfs(gr, v, order, marked)
    order.append(start)


def dfs_by_order(gr, start, marked, component):
    marked.add(start)
    component.append(start)
    for v in neighbors(gr, start):
        if v not in marked:
            dfs_by_order(gr, start, marked, component)


class GraphClass:

    def _paths(self):
        paths = {}
        for v in self.Graph.nodes:
            paths[v] = paths_bfs(self.Graph, v)
        return paths

    def __init__(self, path):
        self.Graph = parse_graph_from_gexf(path)
        self.Paths = self._paths()

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

    def eccentricity(self):
        e = [0 for _ in range(len(self.nodes()))]
        for i, v1 in enumerate(self.nodes()):
            for v2 in self.nodes():
                e[i] = max(e[i], self.Paths[v1][v2])
        return e
