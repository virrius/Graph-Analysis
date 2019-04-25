from Graph_methods import GraphClass
import networkx as nx


Graph = GraphClass("vk.gexf")
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
