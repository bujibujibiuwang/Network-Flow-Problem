import gurobipy as gp
import networkx as nx
import matplotlib.pyplot as plt
from gurobipy import GRB
import pandas as pd

"""
已知数据
"""
factories = dict({'Liverpool': 150000, 'Brighton': 200000})
depots = dict({'Newcastle': 70000, 'Birmingham': 50000, 'London': 100000, 'Exeter': 40000})
customers = dict({'C1': 50000, 'C2': 10000, 'C3': 40000, 'C4': 35000, 'C5': 60000, 'C6': 20000})
edges = {
    ('Liverpool', 'Newcastle'): 0.5,
    ('Liverpool', 'Birmingham'): 0.5,
    ('Liverpool', 'London'): 1.0,
    ('Liverpool', 'Exeter'): 0.2,
    ('Liverpool', 'C1'): 1.0,
    ('Liverpool', 'C3'): 1.5,
    ('Liverpool', 'C4'): 2.0,
    ('Liverpool', 'C6'): 1.0,
    ('Brighton', 'Birmingham'): 0.3,
    ('Brighton', 'London'): 0.5,
    ('Brighton', 'Exeter'): 0.2,
    ('Brighton', 'C1'): 2.0,
    ('Newcastle', 'C2'): 1.5,
    ('Newcastle', 'C3'): 0.5,
    ('Newcastle', 'C5'): 1.5,
    ('Newcastle', 'C6'): 1.0,
    ('Birmingham', 'C1'): 1.0,
    ('Birmingham', 'C2'): 0.5,
    ('Birmingham', 'C3'): 0.5,
    ('Birmingham', 'C4'): 1.0,
    ('Birmingham', 'C5'): 0.5,
    ('London', 'C2'): 1.5,
    ('London', 'C3'): 2.0,
    ('London', 'C5'): 0.5,
    ('London', 'C6'): 1.5,
    ('Exeter', 'C3'): 0.2,
    ('Exeter', 'C4'): 1.5,
    ('Exeter', 'C5'): 0.5,
    ('Exeter', 'C6'): 1.5}
"""
(1)决策变量和目标函数
"""
cost_flow = gp.Model()
flow = cost_flow.addVars(list(edges), vtype=GRB.CONTINUOUS, name='x')
cost_flow.setObjective(flow.prod(edges), GRB.MINIMIZE)
"""
(2)约束条件
"""
# factory constraints
cost_flow.addConstrs(flow.sum(i, '*') <= factories[i] for i in factories.keys())
# depots constraints
cost_flow.addConstrs(flow.sum(i, '*') <= depots[i] for i in depots.keys())
# customers constraints
cost_flow.addConstrs(flow.sum('*', i) == customers[i] for i in customers.keys())
# flow constraints
cost_flow.addConstrs(flow.sum('*', i) == flow.sum(i, '*') for i in depots.keys())
"""
(3)模型求解和结果
"""
cost_flow.optimize()
product_flow = pd.DataFrame(columns=['From', 'To', 'Flow'])
for edge in edges:
    if flow[edge].x > 1e-6:
        product_flow = product_flow.append({'From': edge[0], 'To':edge[1], 'Flow': int(flow[edge].x)}, ignore_index=True)
print(product_flow)


def draw_network_graph():
    graph = nx.DiGraph(list(edges))
    pos = {'Liverpool': (0, 4), 'Brighton': (0, -2),
           'Newcastle': (1, 3), 'Birmingham': (1, 6), 'London': (1, 0), 'Exeter': (1, -3),
           'C1': (2, 0), 'C2': (2, 2), 'C3': (2, 4), 'C4': (2, -2), 'C5': (2, -4), 'C6': (2, 6)}
    plt.subplots(figsize=(10, 5))
    positive_edges = [(u, v) for u, v in graph.edges if flow[u, v].x > 1e-6]
    graph.remove_edges_from([(u, v) for u, v in graph.edges if flow[u, v].x == 0])
    nx.draw_networkx_edges(graph, pos, edgelist=positive_edges, width=1.0, alpha=0.5)
    edge_labels = {(u, v): f"{int(flow[u, v].x)}" for u, v in graph.edges if flow[u, v].x > 1e-6}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='black')
    nx.draw_networkx(graph, pos, node_size=1000, font_size=6)
    plt.show()


draw_network_graph()


