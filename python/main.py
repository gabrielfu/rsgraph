import os
import numpy as np
import matplotlib.pyplot as plt
os.environ["RUST_BACKTRACE"] = "full"

from benchmark import benchmark
import algorithms
import rugraph


print("Edmonds-Karp")
n = 32
rng = np.random.default_rng(seed=0)
capacity = rng.integers(low=0, high=8, size=(n, n)).astype(np.float64)
s = 0
t = 27
benchmark(lambda: algorithms.edmonds_karp(capacity, s, t), name="python")
benchmark(lambda: rugraph.edmonds_karp(capacity, s, t), name="rust")
print()
