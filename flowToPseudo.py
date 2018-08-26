import json
import networkx as nx
import matplotlib.pyplot as plt

from pprint import pprint
	
with open('flowchart.json') as f:
    data = json.load(f)
G = nx.DiGraph()

Nodes_all = data[u'nodes']
for node in Nodes_all:
	G.add_node(node[u'id'], info=node[u'text'])
Edges = data[u'edges']
for edge in Edges:
	G.add_edge(edge[u'source'], edge[u'target'], label=edge[u'label'])
#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()
print(G.nodes[u'start'])
print(G[u'question1'])

