import sys
import itertools

from copy import deepcopy

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = deepcopy(nodes)
        self.edges = deepcopy(edges)
        self.alist = {v: set() for v in nodes}
        for edge in edges.keys():
            self.alist[edge[0]].add(edge[1])
    def update(self):
        alist2 = {v: set() for v in self.nodes}
        for edge in self.edges.keys():
            alist2[edge[0]].add(edge[1])
        self.alist = deepcopy(alist2)


def dfs(G, vertice, visited, parent):
    visited[vertice] = True
    temp = G.alist[vertice]
    for nei in temp:
        if not visited[nei]:
            parent[nei] = vertice
            dfs(G, nei, visited, parent)


def SVE(G, R, terminals):
    V = G.nodes.difference(terminals)
    flag = True;
    for i in range(0, len(V) + 1):
        subs = map(set, itertools.combinations(V, i))
        for sub in subs:
            checkingVertices = sub.union(terminals)
            visited = {v:True for v in G.nodes}
            for v in checkingVertices:
                visited[v] = False;
            parent = {}
            dfs(G, R, visited, parent)
            
            if (all(visited[s] == True for s in visited.keys())):
                nodes = set(parent.keys()).union({R})
                edges = {}
                for key in parent.keys():
                    edges[(parent[key], key)] = G.edges[(parent[key], key)]
                    edges[(key, parent[key])] = G.edges[(parent[key], key)]
                T = Graph(nodes, edges)
                return T
    print "Unreachable!!!"
    exit(0)

