import numpy as np
from typing import List


def edmonds_karp(capacity: np.ndarray, s: int, t: int) -> float:
    # Edmonds Karp maximum flow algorithm
    V = len(capacity)
    flow = 0
    residual = np.zeros((V, V))

    while True:
        # BFS
        q = [s]
        p = np.zeros(V, dtype=int) - 1
        df = float("inf")
        while q:
            u = q.pop(0)
            for v in range(V):
                if capacity[u, v] > 0 and capacity[u, v] > residual[u, v] and p[v] == -1:
                    p[v] = u
                    df = min(df, capacity[u, v] - residual[u, v])
                    if v != t:
                        q.append(v)

        if p[t] >= 0:
            flow += df
            v = t
            while v != s:
                u = p[v]
                residual[u, v] += df
                residual[v, u] -= df
                v = u
        else:
            break

    return flow


