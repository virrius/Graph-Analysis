from Graph_methods import GraphClass, get_undirected_subgraph, graph_coefficients, graph_metrics, eigen, adj_list
import matplotlib.pyplot as plt
import networkx as nx


Graph = GraphClass("data/vk.gexf")
adj_list(Graph)
weak_components = [c for c in Graph.get_weak_connectivity()]
strong_components = [c for c in Graph.get_strong_connectivity()]
weak_comp_lengths = [len(v) for v in weak_components]
strong_comp_lengths = [len(v) for v in strong_components]
print("Компоненты слабой связности: \n", weak_components)
print("Компоненты сильной связности: \n", strong_components)
print("Число компонент слабой связности: ", len(weak_components))
print("Число компонент сильной связности: ", len(strong_components))
print("Число вершин в каждой из компонент слабой связности: \n", weak_comp_lengths)
print("Число вершин в каждой из компонент сильной связности: \n", strong_comp_lengths)
print("Доля узлов в наибольшей компоненте слабой связности: ", max(weak_comp_lengths) / len(Graph.nodes()) * 100, "%")


'''2 TASK'''


Graph.Graph = get_undirected_subgraph(Graph, max(weak_components))

degrees = {}
degrees_sum = 0
for node in Graph.nodes():
    if Graph.degree(node) in degrees:
        degrees[Graph.degree(node)] += 1
    else:
        degrees[Graph.degree(node)] = 1
    degrees_sum += Graph.degree(node)
bins = max(degrees.values())
plt.hist(degrees.keys(), bins=max(degrees.keys()), weights=[i/len(Graph.nodes()) for i in degrees.values()], color="g")
plt.xlabel("Степени вершин")
plt.ylabel("Вероятностное распределение")
plt.savefig("hist.png")
#plt.show()


print("Средняя степень вершины: ", degrees_sum/len(Graph.nodes()))

print("Диаметр графа: ", max(Graph.eccentricity()))
print("Радиус графа: ", min(Graph.eccentricity()))
print("центральные вершины: ", [v for i, v in enumerate(Graph.nodes())
                                if Graph.eccentricity()[i]==min(Graph.eccentricity())])
print("Периферийные вершины: ", [v for i, v in enumerate(Graph.nodes())
                                 if Graph.eccentricity()[i]==max(Graph.eccentricity())])


path_sum = 0
for v1 in Graph.nodes():
    for v2 in Graph.nodes():
        path_sum += Graph.Paths[v1][v2]


'''3 TASK'''
x, y = list(Graph.Graph)[5], list(Graph.Graph)[1]
print("Для вершин: ", x, ", "+y)
print('Число общих соседей: ', Graph.nodes_common_neighbours(x, y))
print('Мера Жакара: ', Graph.nodes_jaccard_coeffitients(x, y))
print('Frequency-Weighted Common Neighbors: ', Graph.nodes_adamic_adar(x, y))
print('Preferential Attachment: ', Graph.nodes_preferential_attachment(x, y))

graph_coefficients(Graph)
graph_metrics(Graph)
eigen(Graph)
