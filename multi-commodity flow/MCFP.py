import gurobipy as gp
import networkx as nx
import matplotlib.pyplot as plt
from gurobipy import GRB

"""
已知数据
"""
commodities = ["Pencils", "Pens"]
points = {"Detroit": (0, 0), "Denver": (0, 1), "Boston": (1, -1), "New York": (1, 1), "Seattle": (1, 3)}

edges = {("Detroit", "Boston"): 100, ("Detroit", "New York"): 80, ("Detroit", "Seattle"): 120,
         ("Denver", "Boston"): 120, ("Denver", "New York"): 120,  ("Denver", "Seattle"): 120}

cost = {("Pencils", "Detroit", "Boston"): 10, ("Pencils", "Detroit", "New York"): 20,
        ("Pencils", "Detroit", "Seattle"): 60, ("Pencils", "Denver", "Boston"): 40,
        ("Pencils", "Denver", "New York"): 40, ("Pencils", "Denver", "Seattle"): 30,
        ("Pens", "Detroit", "Boston"): 20, ("Pens", "Detroit", "New York"): 20,
        ("Pens", "Detroit", "Seattle"): 80, ("Pens", "Denver", "Boston"): 60,
        ("Pens", "Denver", "New York"): 70, ("Pens", "Denver", "Seattle"): 30}

# inflow= supply-demand
# 如果分开写在约束里会出现索引错误，因为不是所有节点对每个商品都有供应和需求
inflow = {("Pencils", "Detroit"): 50, ("Pencils", "Denver"): 60, ("Pens", "Detroit"): 60, ("Pens", "Denver"): 40,
          ("Pencils", "Boston"): -50, ("Pencils", "New York"): -50, ("Pencils", "Seattle"): -10,
          ("Pens", "Boston"): -40, ("Pens", "New York"): -30, ("Pens", "Seattle"): -30}

"""
(1)变量和目标
"""
multi_commodity = gp.Model()
flow = multi_commodity.addVars(list(cost), vtype=GRB.CONTINUOUS)
multi_commodity.setObjective(flow.prod(cost), GRB.MINIMIZE)
"""
(2)约束条件
"""
# 容量约束
multi_commodity.addConstrs(flow.sum('*', u, v) <= edges[(u, v)] for u, v in edges.keys())
# 流平衡约束
multi_commodity.addConstrs(flow.sum(h, '*', v) + inflow[h, v] == flow.sum(h, v, '*')
                           for h in commodities for v in points.keys())
"""
(3)求解模型
"""
multi_commodity.optimize()
for h in commodities:
    for u, v in edges.keys():
        if flow[h, u, v].x > 1e-6:
            print(f'{h} {u} >> {v}:{int(flow[h, u, v].x)}')


def draw_network_graph():
    graph = nx.DiGraph(list(edges))
    plt.subplots(figsize=(8, 6))
    edge_labels = {(u, v): f"{[int(flow[h, u, v].x) for h in commodities ]}" for u, v in graph.edges}
    nx.draw_networkx_edge_labels(graph, points, edge_labels=edge_labels, font_color='black')
    nx.draw_networkx(graph, pos=points, node_size=1000, font_size=6)
    plt.show()


draw_network_graph()