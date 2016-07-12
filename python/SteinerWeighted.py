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


def floyd(G):
    d = {(i,j):sys.maxint for i in G.nodes  for j in G.nodes}
    for i in G.nodes:
        d[(i,i)] = 0
    
    for a in G.edges.keys():
        d[a] = G.edges[a]
    
    for k in G.nodes:
        for i in G.nodes:
            for j in G.nodes:
                d[(i, j)] = min(d[(i,j)], d[(i, k)] + d[(k, j)])
    return d

def steinerPrim(nodes, distances, R):
    g = {}
    e = {}
    S = set()
    z = 0
    T = Graph(nodes, {})
    for v in nodes:
        g[v] = sys.maxint
    g[R] = 0
    while len(S)!=len(nodes):
        VmS = nodes.difference(S)
        g2 = {i: g[i] for i in VmS}
        i = min(g2, key = g2.get)
        
        if g2[i] == sys.maxint:
            z = sys.maxint
            break
        z = z + g2[i]
        S.update({i})
        if i != R:
            T.edges[e[i]] = distances[e[i]]
            T.edges[e[i][1], e[i][0]] = distances[e[i]]
        VmS.remove(i)
        for j in VmS:
            if(g[j] > distances[(i, j)]):
                g[j] = distances[(i, j)]
                e[j] = (i, j)
    return T, z

def dijkstra(s, t, G):
    Q = {v for v in G.nodes}
    dist = {v:sys.maxint for v in G.nodes}
    prev = {v: -1 for v in G.nodes}

    dist[s] = 0

    while(len(Q) > 0):
        dist2 = {v:dist[v] for v in Q}
        u = min(dist2, key = dist2.get)
        if u == t:
            break
        Q.remove(u)
        for nei in G.alist[u]:
            alt = dist[u] + G.edges[(u, nei)]
            if(alt < dist[nei]):
                dist[nei] = alt
                prev[nei] = u

    return prev

def correct(T, G, edge):
    T.edges.pop(edge)
    T.edges.pop(edge[1], edge[0])
    s = edge[0]
    t = edge[1]
    prev = dijkstra(s, t, G)
    while s!=t:
        T.nodes.update({prev[t]})
        T.edges[(prev[t], t)] = G.edges[(prev[t], t)]
        T.edges[(t, prev[t])] = G.edges[(prev[t], t)]
        t = prev[t]
    T.update()

def weightedSteiner(G, R, terminals):
    d = floyd(G)
    terminals = terminals.union({R})
    S = G.nodes.difference(terminals)
    W = sys.maxint
    for i in range(1, len(terminals)):
        subs = map(set, itertools.combinations(S, i))
        for sub in subs:
            Tprime, z = steinerPrim(terminals.union(sub), d, R)
            if z < W:
                W = z
                T = Tprime
    if W!=sys.maxint:
        Tresult = T
        for edge in Tresult.edges.keys():
            if edge not in G.edges.keys() or Tresult.edges[edge] < G.edges[edge]:
                correct(Tresult, G, edge)
        Tresult.update()
        return Tresult
    print "Unreachable!!"
    exit(0)

