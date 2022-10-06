from dis import dis
import numpy as np
import time
import scipy.stats
import pyemd
import matplotlib.pyplot as plt
import pandas as pd
import naive
import rust_emd

# setup
def test(n=1000):
    # setup
    seed = 0
    rng = np.random.default_rng(seed)
    arr1 = rng.uniform(size=n) 
    arr2 = rng.uniform(size=n) 
    arr1 /= arr1.sum()
    arr2 /= arr2.sum()

    result = {"n": n}

    # scipy
    t0 = time.perf_counter()
    bins = np.arange(n)
    dist = scipy.stats.wasserstein_distance(bins, bins, arr1, arr2)
    t1 = time.perf_counter()
    result["scipy"] = t1 - t0

    # naive
    t0 = time.perf_counter()
    dist = naive.wasserstein(arr1, arr2)
    t1 = time.perf_counter()
    result["naive"] = t1 - t0
    return result

result = []
for n in [10, 20, 50, 100, 200, 500, 1000, 2000]:
    result.append(test(n))

df = pd.DataFrame(result)
print(df)

    
# print("====== scipy ======")
# print(f"time: {t1-t0:.6f}s")
# print(f"distance: {dist:.4f}")