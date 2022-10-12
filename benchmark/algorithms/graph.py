import numpy as np
from typing import Set, List

class Edge:
    def __init__(self, src: int, dest: int, weight: float):
        self.src = src
        self.dest = dest
        self.weight = weight

class Graph:
    def __init__(self):
        self.v: int = 0
        self.e: int = 0
        self.nodes: Set = set()
        self.edges: List[Edge] = []

    def _add_node(self, node: int):
        if node not in self.nodes:
            self.nodes.add(node)
            self.v += 1

    def add_edge(self, src: int, dest: int, weight: float):
        self._add_node(src)
        self._add_node(dest)
        self.edges.append(Edge(src, dest, weight))
        self.e += 1

    @classmethod
    def from_adj_matrix(cls, adj: np.ndarray) -> "Graph":
        g = cls()
        n = len(adj)
        for i in range(n):
            for j in range(n):
                g.add_edge(i, j, adj[i][j])
        return g