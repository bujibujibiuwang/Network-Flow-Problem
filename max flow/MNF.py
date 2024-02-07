import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import matplotlib.pyplot as plt

points = {'s': (0, 1), 'a': (1, 2), 'b': (3, 2), 'c': (2, 1), 'd': (1, 0), 'e': (3, 0), 't': (4, 1)}
edges = {('a', 'b'): 13, ('c', 'b'): 2, ('b', 't'): 8, ('a', 'c'): 3,
         ('c', 'e'): 8, ('d', 'c'): 7, ('d', 'e'): 5, ('e', 't'): 12,
         ('s', 'a'): 6, ('s', 'c'): 7, ('s', 'd'): 11}


maxflow = gp.Model()
flow = maxflow.addVars(edges.keys(), vtype=GRB.CONTINUOUS)
maxflow.setObjective(flow.sum('*', 't'), GRB.MAXIMIZE)
maxflow.addConstrs(flow[i, j] <= edges[i, j] for i, j in edges.keys())
maxflow.addConstrs(flow.sum('*', i) - flow.sum(i, '*') == 0 for i in points.keys() if i != 's' and i != 't')
maxflow.optimize()

for i, j in edges.keys():
    print(flow[i, j].x)


def draw_network_graph():
    graph = nx.DiGraph(list(edges))
    plt.subplots(figsize=(10, 5))
    edge_labels = {(u, v): f"{edges[(u, v)]}/{int(flow[u, v].x)}" for u, v in graph.edges}
    nx.draw_networkx_edge_labels(graph, points, edge_labels=edge_labels, font_color='black')
    nx.draw_networkx(graph, pos=points)
    plt.show()


draw_network_graph()