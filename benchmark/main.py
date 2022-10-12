import os
import numpy as np
import matplotlib.pyplot as plt
os.environ["RUST_BACKTRACE"] = "full"

from benchmark import benchmark
import algorithms
from algorithms.graph import Graph
import rsgraph
import networkx as nx
from networkx.exception import NetworkXUnbounded


def benchmark_edmonds_karp():
    print("Benchmarking: Edmonds-Karp")
    
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
    
    n = 32
    capacity, s, t = setup(n)
    print(f"Graph size: {n}")
    
    def nx_flow():
        G = nx.from_numpy_array(capacity, create_using=nx.DiGraph())
        return nx.maximum_flow_value(G, s, t, capacity="weight")
    
    def nx_ek():
        G = nx.from_numpy_array(capacity, create_using=nx.DiGraph())
        return nx.algorithms.flow.edmonds_karp(G, s, t, capacity="weight").graph["flow_value"]
    
    def python():
        return algorithms.edmonds_karp(capacity, s, t)
    
    def rust():
        return rsgraph.edmonds_karp(capacity, s, t)
    
    func_dict = {
        "nx_flow": nx_flow,
        "nx_ek": nx_ek,
        "python": python,
        "rust": rust,
    }

    # Benchmark
    for name, func in func_dict.items():
        benchmark(func, name=name)
    print()
    

def benchmark_bellman_ford():
    print("Benchmarking: Bellman-Ford")
    
    def setup(n):
        rng = np.random.default_rng(seed=0)
        adj = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
        source = 0
        return adj, source

    n = 32
    adj, source = setup(n)
    print(f"Graph size: {n}")
    
    def nx_bf():
        try:
            G = nx.from_numpy_array(adj, create_using=nx.DiGraph())
            return nx.single_source_bellman_ford(G, source)
        except NetworkXUnbounded:
            return None

    def python():
        try:
            g = Graph.from_adj_matrix(adj)
            return algorithms.bellman_ford(g, source)
        except algorithms.NegativeCycleException:
            return None

    def rust():
        try:
            return rsgraph.bellman_ford(adj, source)
        except rsgraph.NegativeCycleException:
            return None
    
    func_dict = {
        "nx_bf": nx_bf,
        "python": python,
        "rust": rust,
    }

    # Benchmark
    for name, func in func_dict.items():
        benchmark(func, name=name)
    print()


if __name__ == "__main__":
    benchmark_edmonds_karp()
    benchmark_bellman_ford()
