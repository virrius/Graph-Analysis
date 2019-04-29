from networkx import *
from collections import deque
from collections import defaultdict
from math import log


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


def paths_bfs(gr, start, v=None):
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


def count_shortest_paths_with_keypoint(gr, start, keypoint):
    visited = set()
    queue = deque()
    queue.append(start)
    layer_queue = deque()
    paths_count = 1
    keypoint_visited = set()
    keypoint_visited.add(keypoint)
    tmp = False
    c=0

    while queue or layer_queue:

        if not queue:
            queue.extend(list(layer_queue))
            if(keypoint in queue):
                queue.appendleft(keypoint)
            layer_queue.clear()

        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            if vertex in keypoint_visited:
                paths_count += 1
                keypoint_visited.update(set(neighbors(gr, vertex)))
                keypoint_visited= keypoint_visited - visited
                queue.extendleft(keypoint_visited)
            else:
                layer_queue.extend(set(neighbors(gr, vertex)) - visited)


    print(c)
    return paths_count


def ordered_dfs(gr, start, order, marked):

    marked.add(start)
    for v in neighbors(gr, start):
        if v not in marked:
            ordered_dfs(gr, v, order, marked)
    order.append(start)


def graph_coefficients(graph):
    file = open('coefficients.txt', 'w')
    file.write("---------------Common neighbours--------------- \n\n")
    for v1 in graph.nodes():
        for v2 in graph.nodes():
            if v1 != v2:
                file.write(v1+' '+v2+' -> '+str(graph.nodes_common_neighbours(v1, v2)) + '\n')

    file.write("\n\n---------------Jaccard’s Coefficient--------------- \n\n")
    for v1 in graph.nodes():
        for v2 in graph.nodes():
            if v1 != v2:
                file.write(v1 + ' ' + v2 + ' -> ' + str(graph.nodes_jaccard_coeffitients(v1, v2)) + '\n')

    file.write("\n\n---------------Adamic/Adar (Frequency-Weighted Common Neighbors)--------------- \n\n")
    for v1 in graph.nodes():
        for v2 in graph.nodes():
            if v1 != v2:
                file.write(v1 + ' ' + v2 + ' -> ' + str(graph.nodes_adamic_adar(v1, v2)) + '\n')

    file.write("\n\n---------------preferential_attachment--------------- \n\n")
    for v1 in graph.nodes():
        for v2 in graph.nodes():
            if v1 != v2:
                file.write(v1 + ' ' + v2 + ' -> ' + str(graph.nodes_preferential_attachment(v1, v2)) + '\n')


def graph_metrics(graph):
    file = open('metrics.txt', 'w')
    file.write("---------------degree centrality--------------- \n\n")
    for v in graph.nodes():
        file.write(v + ' -> ' + str(graph.degree(v)/len(graph.nodes())) + '\n')

    file.write("\n\n---------------closeness centrality--------------- \n\n")
    for v in graph.nodes():
        sum = 0
        for v1 in graph.nodes():
            sum += graph.Paths[v][v1]
        file.write(v + ' -> ' + str(len(graph.nodes())/sum) + '\n')

    file.write("\n\n---------------closeness centrality--------------- \n\n")

    for key_v in graph.nodes():
        sum = 0
        for v1 in graph.nodes():

            if v1 != key_v:

                sum += count_shortest_paths_with_keypoint(graph.Graph,v1,key_v)
        file.write(key_v + ' -> ' + str(sum/len(graph.nodes())) + '\n')




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

    def nodes_common_neighbours(self, node1, node2):
        return len(set(neighbors(self.Graph, node1)) & set(neighbors(self.Graph, node2)))

    def nodes_jaccard_coeffitients(self, node1, node2):
        return self.nodes_common_neighbours(node1, node2)/len(set(neighbors(self.Graph, node1)) |
                                                                   set(neighbors(self.Graph, node2)))

    def nodes_adamic_adar(self, node1, node2):
        return sum(1 / log(self.degree(w)) for w in set(neighbors(self.Graph, node1)) &
                                                    set(neighbors(self.Graph, node2)))

    def nodes_preferential_attachment(self, node1, node2):
        return self.degree(node1) * self.degree(node2)
