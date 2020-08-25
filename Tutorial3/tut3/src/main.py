import networkx as nx
from collections import Counter 
#import matplotlib.pyplot as plt
import itertools
import operator

key_players = []

G = nx.read_gml("../../football/football.gml");

print("Number of nodes: ");
number_of_nodes = len(G.nodes())
print(str(number_of_nodes));

print("\nNumber of axis: ");
number_of_edges = len(G.edges())
print(str(number_of_edges));

print("\nDensity:");
max_edges = (number_of_nodes * (number_of_nodes - 1)) / 2;
print(number_of_edges/max_edges);

print("\nConnectivity:");
print(len(nx.minimum_node_cut(G)));

print("\n\nCentrality\nDegree:");
degree = Counter(nx.degree_centrality(G)).most_common(3);
key_players.extend([node for (node, deg) in degree]);
print(degree);


print("\nCloseness:");
close = Counter(nx.closeness_centrality(G)).most_common(3);
key_players.extend([node for (node, c) in close]);
print(close);

print("\nBetweenness:");
bet = Counter(nx.betweenness_centrality(G)).most_common(3);
key_players.extend([node for (node, b) in bet]);
print(bet);

print("\nEigenvector:");
eigen = Counter(nx.eigenvector_centrality(G)).most_common(3);
key_players.extend([node for (node, e) in eigen]);
print(eigen);

print("\nClusters:");
clus = Counter(nx.clustering(G)).most_common(3);
#key_players.extend([node for (node, c) in clus]);
print(clus);

for node in key_players:
	G.node[node]['viz'] = {'color': {'r': 255, 'g': 0, 'b': 0, 'a': 0}}

nx.write_gexf(G, "export.gexf")