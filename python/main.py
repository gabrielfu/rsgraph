import os
import numpy as np
import matplotlib.pyplot as plt
os.environ["RUST_BACKTRACE"] = "full"

from benchmark import benchmark
import algorithms
import rugraph


n = 32
rng = np.random.default_rng(seed=0)
path = rng.integers(low=0, high=8, size=(n, n)).astype(np.float64)
s = 0
t = 27

print(f"python output: {algorithms.edmonds_karp(path, s, t)}")
print(f"rust output: {rugraph.edmonds_karp(path, s, t)}")

benchmark(lambda: algorithms.edmonds_karp(path, s, t), name="python")
benchmark(lambda: rugraph.edmonds_karp(path, s, t), name="rust")

# import timeit

# timeit.main(args="algorithms.edmonds_karp(path, s, t)")
# timeit.main(args="rugraph.edmonds_karp(path, s, t)")