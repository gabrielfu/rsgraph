from typing import List

def edmond_karp(path: List[List[int]], s: int, t: int) -> float:
    # Edmonds Karp maximum flow algorithm
    V = len(path)
    flow = 0
    residual = [[0] * V for _ in range(V)]

    while True:
        # BFS
        q = [s]
        p = [None] * V
        df = float("inf")
        while q:
            u = q.pop(0)
            for v in range(V):
                if path[u][v] > 0 and path[u][v] > residual[u][v] and p[v] is None:
                    p[v] = u
                    df = min(df, path[u][v] - residual[u][v])
                    if v != t:
                        q.append(v)

        if p[t] is not None:
            flow += df
            v = t
            while v != s:
                u = p[v]
                residual[u][v] += df
                residual[v][u] -= df
                v = u
        else:
            break

    return flow


