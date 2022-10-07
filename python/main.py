import os
import numpy as np
import matplotlib.pyplot as plt
os.environ["RUST_BACKTRACE"] = "full"

from benchmark import benchmark
import algorithms
import rugraph
import networkx as nx


def benchmark_edmonds_karp():
    print("Benchmarking: Edmonds-Karp")
    
    # setup
    n = 32
    rng = np.random.default_rng(seed=0)
    capacity = rng.integers(low=0, high=16, size=(n, n)).astype(np.float64)
    s = 0
    t = 27

    # no loop
    capacity[np.diag_indices(n)] = 0
    # uni-directional graph
    capacity[np.tril_indices(n)] = 0
    # sink exits completely
    capacity[t] = 0
    # source is sole entrance
    capacity[:, s] = 0

    G = nx.from_numpy_array(capacity, create_using=nx.DiGraph())
    print("Validating output: nx_flow={nx_flow}, nx_ek={nx_ek}, python={python}, rust={rust}".format(
        nx_flow=nx.maximum_flow_value(G, s, t, capacity="weight"),
        nx_ek=nx.algorithms.flow.edmonds_karp(G, s, t, capacity="weight").graph["flow_value"],
        python=algorithms.edmonds_karp(capacity, s, t),
        rust=rugraph.edmonds_karp(capacity, s, t),
    ))

    benchmark(lambda: nx.maximum_flow_value(G, s, t, capacity="weight"), name="nx_flow")
    benchmark(lambda: nx.algorithms.flow.edmonds_karp(G, s, t, capacity="weight"), name="nx_ek")
    benchmark(lambda: algorithms.edmonds_karp(capacity, s, t), name="python")
    benchmark(lambda: rugraph.edmonds_karp(capacity, s, t), name="rust")
    print()


if __name__ == "__main__":
    benchmark_edmonds_karp()
