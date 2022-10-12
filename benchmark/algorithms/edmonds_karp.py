import numpy as np


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


# def edmonds_karp(C: np.ndarray, s: int, t: int) -> float:
#         n = len(C) # C is the capacity matrix
#         F = [[0] * n for i in range(n)]
#         path = bfs(C, F, s, t)
#       #  print path
#         while path != None:
#             flow = min(C[u][v] - F[u][v] for u,v in path)
#             for u,v in path:
#                 F[u][v] += flow
#                 F[v][u] -= flow
#             path = bfs(C, F, s, t)
#         return sum(F[s][i] for i in range(n))

# #find path by using BFS
# def bfs(C, F, s, t):
#         queue = [s]
#         paths = {s:[]}
#         if s == t:
#             return paths[s]
#         while queue: 
#             u = queue.pop(0)
#             for v in range(len(C)):
#                     if(C[u][v]-F[u][v]>0) and v not in paths:
#                         paths[v] = paths[u]+[(u,v)]
#                         if v == t:
#                             return paths[v]
#                         queue.append(v)
#         return None
