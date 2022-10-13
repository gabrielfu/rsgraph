import os
import numpy as np
import matplotlib.pyplot as plt
os.environ["RUST_BACKTRACE"] = "full"

import perfplot
from formats import format_perf_data, format_snake_case
import algorithms
from algorithms.graph import Graph
import rsgraph
import networkx as nx
from networkx.exception import NetworkXUnbounded


def benchmark_edmonds_karp():
    name = "Edmonds-Karp Algorithm"
    print(f"Benchmarking: {name}")
    
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
    
    def nx_func(capacity, s, t):
        G = nx.from_numpy_array(capacity, create_using=nx.DiGraph())
        return nx.algorithms.flow.edmonds_karp(G, s, t, capacity="weight").graph["flow_value"]
    
    def py_func(capacity, s, t):
        return algorithms.edmonds_karp(capacity, s, t)
    
    def rsgraph_func(capacity, s, t):
        return rsgraph.edmonds_karp(capacity, s, t)
    
    perf_data = perfplot.bench(
        setup=setup,
        kernels=[nx_func, py_func, rsgraph_func],
        labels=["networkx", "python", "rsgraph"],
        n_range=[2 ** k for k in range(2, 10)],
        xlabel="graph size",
        equality_check=None,
    )
    print(format_perf_data(perf_data))
    perf_data.title = name
    perf_data.save(
        filename=f"./images/perf_{format_snake_case(name)}.png",
        logx=True,
        logy=True,
        transparent=False,
        bbox_inches="tight",
    )
    

def benchmark_bellman_ford():
    name = "Bellman-Ford Algorithm"
    print(f"Benchmarking: {name}")
    
    def setup(n):
        rng = np.random.default_rng(seed=0)
        adj = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
        source = 0
        return adj, source
    
    def nx_func(adj, source):
        try:
            G = nx.from_numpy_array(adj, create_using=nx.DiGraph())
            return nx.single_source_bellman_ford(G, source)
        except NetworkXUnbounded:
            return None

    def py_func(adj, source):
        try:
            g = Graph.from_adj_matrix(adj)
            return algorithms.bellman_ford(g, source)
        except algorithms.NegativeCycleException:
            return None

    def rsgraph_func(adj, source):
        try:
            return rsgraph.bellman_ford(adj, source)
        except rsgraph.NegativeCycleException:
            return None
    
    perf_data = perfplot.bench(
        setup=setup,
        kernels=[nx_func, py_func, rsgraph_func],
        labels=["networkx", "python", "rsgraph"],
        n_range=[2 ** k for k in range(2, 10)],
        xlabel="graph size",
        equality_check=None,
    )
    print(format_perf_data(perf_data))
    perf_data.title = name
    perf_data.save(
        filename=f"./images/perf_{format_snake_case(name)}.png",
        logx=True,
        logy=True,
        transparent=False,
        bbox_inches="tight",
    )
    

def benchmark_kruskal():
    name = "Kruskal's Algorithm"
    print(f"Benchmarking: {name}")

    def setup(n):
        rng = np.random.default_rng(seed=0)
        adj = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
        # undirected graph
        adj[np.tril_indices(n, -1)] = adj.T[np.tril_indices(n, -1)]
        # no loop
        adj[np.diag_indices(n)] = 0
        return adj

    def nx_func(adj):
        G = nx.from_numpy_array(adj, create_using=nx.Graph())
        mst = nx.minimum_spanning_tree(G)
        mst = nx.to_numpy_array(mst)
        return mst

    def rsgraph_func(adj):
        mst = rsgraph.kruskal(adj)
        return mst
    
    perf_data = perfplot.bench(
        setup=setup,
        kernels=[nx_func, rsgraph_func],
        labels=["networkx", "rsgraph"],
        n_range=[2 ** k for k in range(2, 10)],
        xlabel="graph size",
        equality_check=None,
    )
    print(format_perf_data(perf_data))
    perf_data.title = name
    perf_data.save(
        filename=f"./images/perf_{format_snake_case(name)}.png",
        logx=True,
        logy=True,
        transparent=False,
        bbox_inches="tight",
    )


if __name__ == "__main__":
    benchmark_edmonds_karp()
    benchmark_bellman_ford()
    benchmark_kruskal()
