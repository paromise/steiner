import numpy, sys, itertools, random
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

def findTrees(G, R, Vbar, K):
    treeCount = 0
    result = set()
    edgeIds = []
    while treeCount != K:
        vSeenCount = 0
        seen = set()
        nextV = R
        toBeSeen = []
        demandingEdges = {}
        edges = {}
        edgeId = set()
        while vSeenCount != len(Vbar):
            if nextV in Vbar:
                vSeenCount += 1
            seen.add(nextV)
            if vSeenCount == len(Vbar):
                break
            for adjV in G.alist[nextV]:
                if adjV not in seen:
                    if adjV not in toBeSeen:
                        toBeSeen.append(adjV)
                        demandingEdges[adjV] = [(adjV, nextV)]
                    else:
                        demandingEdges[adjV].append((adjV, nextV))
            V2 = toBeSeen.pop(random.randint(0, len(toBeSeen) - 1))
            nextEdge = demandingEdges[V2].pop(random.randint(0, len(demandingEdges[V2]) - 1))
            #print nextEdge
            edges[nextEdge] = G.edges[nextEdge]
            edges[(nextEdge[1], nextEdge[0])] = G.edges[nextEdge]
            edgeId.add(G.edges[nextEdge][1])
            nextV = V2
        tree = Graph(seen, edges)
        if edgeId not in edgeIds:
            result.add(tree)
            treeCount += 1
            edgeIds.append(edgeId)
    return result

def root(tree, terminals, R, parents, parent, resNodes):
    leave = R not in terminals
    for child in tree.alist[R]:
        if child != parent:
            parents[child] = R
            if root(tree, terminals, child, parents, R, resNodes):
                leave = False
    if not leave:
        resNodes.add(R)
        #print resNodes
    return not leave
        

def prune(tree, R, terminals):
    parents = {v:-1 for v in tree.nodes}
    resNodes = set()
    a = root(tree, terminals, R, parents, -1, resNodes)
    tree.nodes = resNodes
    edges = {}
    for node in resNodes:
        if parents[node] != -1:
            edges[(node, parents[node])] = tree.edges[(node, parents[node])]
            edges[(parents[node], node)] = tree.edges[(node, parents[node])]
    tree.edges = edges
    tree.update()
    #print tree.nodes
    return len(tree.nodes) - 1
    

def TPH(G, R, K, terminals):
    Vbar = G.nodes
    resSize = sys.maxint
    resTree = G
    nodesList = list(G.nodes)

    while True:
        W = len(Vbar)
        #print Vbar
        trees = findTrees(G, R, Vbar, K)
        for tree in trees:
            size = prune(tree, R, terminals)
            if size < resSize:
                resTree = tree
                resSize = size
        
        Vbar = resTree.nodes
        if W == len(resTree.nodes):
            break
    return resTree

