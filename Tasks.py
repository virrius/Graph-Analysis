from Graph_methods import GraphClass, get_max_connectivity_component
import matplotlib.pyplot as plt

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


Graph.Graph = get_max_connectivity_component(Graph, max(weak_components))

degrees = {}
for node in Graph.nodes():
    print(Graph.degree(node))
    if Graph.degree(node) in degrees:
        degrees[Graph.degree(node)] += 1
    else:
        degrees[Graph.degree(node)] = 1

print(Graph.degree(Graph.nodes()))
bins = max(degrees.values())
print(bins)
print(Graph.nodes())
plt.hist(degrees.keys(), bins=max(degrees.keys()), weights=[i/len(Graph.nodes()) for i in degrees.values()], color="g")
plt.xlabel("Степени вершин")
plt.ylabel("Вероятностное распределение")
plt.savefig("hist.png")




plt.show()



