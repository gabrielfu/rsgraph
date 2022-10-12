from .graph import Graph
from typing import Dict, Tuple, List


class NegativeCycleException(Exception):
    pass


def bellman_ford(g: Graph, src: int) -> Tuple[Dict[int, float], Dict[int, List[int]]]:
    dist = {v: float("inf") for v in g.nodes}
    parents = {v: -1 for v in g.nodes}

    # distance to src is 0
    dist[src] = 0

    # relax edges for |V| - 1 times
    for _ in range(g.v - 1):
        for edge in g.edges:
            u = edge.src
            v = edge.dest
            w = edge.weight
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parents[v] = u

    # check for negative weight cycles
    for edge in g.edges:
        u = edge.src
        v = edge.dest
        w = edge.weight
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            raise NegativeCycleException

    path = {}
    for node in g.nodes:
        node_path = []
        p = node
        while True:
            node_path.insert(0, p)
            if p == src:
                break
            p = parents[p]
        path[node] = node_path

    return dist, path

