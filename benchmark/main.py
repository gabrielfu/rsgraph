import os
os.environ["RUST_BACKTRACE"] = "full"

import numpy as np
import networkx as nx
from networkx.exception import NetworkXUnbounded
import rsgraph
import algorithms
from algorithms.graph import Graph
from bench import Bench, register_kernel


class EdmondsKarpBench(Bench):
    name = "Edmonds-Karp Algorithm"

    @staticmethod
    def setup(n):
        # source
        s = 0
        # sink
        t = n - 1
        # capacity adjacency matrix
        rng = np.random.default_rng(seed=0)
        capacity = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
        # no loop
        capacity[np.diag_indices(n)] = 0
        # uni-directional graph
        capacity[np.tril_indices(n)] = 0
        # sink exits completely
        capacity[t] = 0
        # source is sole entrance
        capacity[:, s] = 0

        return capacity, s, t

    @staticmethod
    @register_kernel(label="networkx")
    def nx_func(capacity, s, t):
        G = nx.from_numpy_array(capacity, create_using=nx.DiGraph())
        return nx.algorithms.flow.edmonds_karp(G, s, t, capacity="weight").graph["flow_value"]

    @staticmethod
    @register_kernel(label="python")
    def py_func(capacity, s, t):
        return algorithms.edmonds_karp(capacity, s, t)

    @staticmethod
    @register_kernel(label="rsgraph")
    def rsgraph_func(capacity, s, t):
        return rsgraph.edmonds_karp(capacity, s, t)


class BellmanFordBench(Bench):
    name = "Bellman-Ford Algorithm"

    @staticmethod
    def setup(n):
        rng = np.random.default_rng(seed=0)
        adj = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
        source = 0
        return adj, source

    @staticmethod
    @register_kernel(label="networkx")
    def nx_func(adj, source):
        try:
            G = nx.from_numpy_array(adj, create_using=nx.DiGraph())
            return nx.single_source_bellman_ford(G, source)
        except NetworkXUnbounded:
            return None

    @staticmethod
    @register_kernel(label="python")
    def py_func(adj, source):
        try:
            g = Graph.from_adj_matrix(adj)
            return algorithms.bellman_ford(g, source)
        except algorithms.NegativeCycleException:
            return None

    @staticmethod
    @register_kernel(label="rsgraph")
    def rsgraph_func(adj, source):
        try:
            return rsgraph.bellman_ford(adj, source)
        except rsgraph.NegativeCycleException:
            return None


class KruskalBench(Bench):
    name = "Kruskal's Algorithm"

    @staticmethod
    def setup(n):
        rng = np.random.default_rng(seed=0)
        adj = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
        # undirected graph
        adj[np.tril_indices(n, -1)] = adj.T[np.tril_indices(n, -1)]
        # no loop
        adj[np.diag_indices(n)] = 0
        return adj

    @staticmethod
    @register_kernel(label="networkx")
    def nx_func(adj):
        G = nx.from_numpy_array(adj, create_using=nx.Graph())
        mst = nx.minimum_spanning_tree(G)
        mst = nx.to_numpy_array(mst)
        return mst

    @staticmethod
    @register_kernel(label="rsgraph")
    def rsgraph_func(adj):
        mst = rsgraph.kruskal(adj)
        return mst


if __name__ == "__main__":
    EdmondsKarpBench.run_benchmark()
    BellmanFordBench.run_benchmark()
    KruskalBench.run_benchmark()
