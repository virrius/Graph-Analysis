from networkx import *
from collections import deque
from collections import defaultdict
from math import log, sqrt

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


def count_shortest_paths_with_keypoint(gr, start, keypoint):
    visited = set()
    queue = deque()
    queue.append(start)
    layer_queue = deque()
    paths_count = 0
    path_length = 0
    keypoint_visited = False

    while queue or layer_queue:
        if not queue:
            queue.extend(list(layer_queue))
            layer_queue.clear()
            path_length += 1

        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            layer_queue.extend(set(neighbors(gr.Graph, vertex)) - visited)
            if keypoint_visited and gr.Paths[start][vertex] >= path_length:
                paths_count += 1
            if vertex == keypoint:
                keypoint_visited = True
                queue.clear()
                layer_queue.clear()
                visited.clear()
                visited.add(keypoint)
                layer_queue.extend(set(neighbors(gr.Graph, vertex)))
                
    return paths_count


def count_shortest_paths_with_edge(gr, start, keypoint1, keypoint2):
    visited = set()
    queue = deque()
    queue.append(start)
    layer_queue = deque()
    paths_count = 0
    path_length = 0
    edge_visited = False

    while queue or layer_queue:
        if not queue:
            queue.extend(list(layer_queue))
            layer_queue.clear()
            path_length += 1

        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            layer_queue.extend(set(neighbors(gr.Graph, vertex)) - visited)
            if edge_visited and gr.Paths[start][vertex] >= path_length:
                paths_count += 1
            if vertex == keypoint1:
                path_length += 1
                edge_visited = True
                queue.clear()
                layer_queue.clear()
                visited.clear()
                visited.add(keypoint1)
                visited.add(keypoint2)
                layer_queue.extend(set(neighbors(gr.Graph, keypoint2))-set(keypoint1))

    return paths_count




def ordered_dfs(gr, start, order, marked):

    marked.add(start)
    for v in neighbors(gr, start):
        if v not in marked:
            ordered_dfs(gr, v, order, marked)
    order.append(start)


def eigen(gr):
    x = {v: 1 for v in gr.Graph}
    max_iter = 50
    for i in range(max_iter):
        last = x
        x = last.copy()
        for n in x:
            for nbr in gr.Graph[n]:
                x[nbr] += last[n]
        norm = sqrt(sum(z ** 2 for z in x.values())) or 1
        x = {k: v / norm for k, v in x.items()}
        if sum(abs(x[n] - last[n]) for n in x) < len(gr.nodes())*1e-6:
            return x


def adj_list(gr):
    file = open('data/adj_list.csv', 'w')
    for v in gr.nodes():
        file.write(v+": "+str([n for n in neighbors(gr.Graph,v)])+"\n")


def graph_coefficients(graph):
    file = open('data/coefficients.txt', 'w')
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
    file = open('data/metrics.txt', 'w')
    file.write("---------------degree centrality--------------- \n\n")
    for v in graph.nodes():
        file.write(v + ' -> ' + str(graph.degree(v)/len(graph.nodes())) + '\n')

    file.write("\n\n---------------closeness centrality--------------- \n\n")
    for v in graph.nodes():
        sum = 0
        for v1 in graph.nodes():
            sum += graph.Paths[v][v1]
        file.write(v + ' -> ' + str(len(graph.nodes())/sum) + '\n')

    file.write("\n\n---------------betweenness centrality--------------- \n\n")

    for key_v in graph.nodes():
        sum = 0
        for v1 in graph.nodes():

            if v1 != key_v:

                sum += count_shortest_paths_with_keypoint(graph,v1,key_v)
        file.write(key_v + ' -> ' + str(sum/(len(graph.nodes())-1)/(len(graph.nodes())-2)*2) + '\n')
    file.write("\n\n---------------eigenvector centrality--------------- \n\n")
    for v, c in eigen(graph).items():
        file.write(str(v) + ' -> ' + str(c) + '\n')
    #print(edge_betweenness_centrality(graph.Graph))
    file.write("\n\n---------------edge betweenness centrality--------------- \n\n")

    visited = set()
    for key_v1 in graph.nodes():
        for key_v2 in graph.nodes():
            sum = 1
            if key_v1 != key_v2 and key_v1 in neighbors(graph.Graph, key_v2) and (key_v1, key_v2) not in visited:
                for v1 in graph.nodes():
                    if v1 != key_v2:
                        sum += count_shortest_paths_with_edge(graph, v1, key_v1, key_v2)
                file.write(key_v1 + " " + key_v2 + ' -> ' + str(sum / (len(graph.nodes())) / (len(graph.nodes()) - 1) * 2) + '\n')
                visited.add((key_v2, key_v1))



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
