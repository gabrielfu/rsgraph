import rsgraphlib
import numpy as np
from typing import Dict, List, Tuple


class NegativeCycleException(Exception):
    pass


def edmonds_karp(capacity: np.ndarray, s: int, t: int) -> float:
    """
    Computes the Edmonds Karp maximum flow algorithm
    
    Args:
        capacity (np.ndarray): 2d adjacency matrix
        s (int): source node
        t (int): sink node
        
    Returns:
        float: maximum flow
    """
    if not isinstance(capacity, np.ndarray):
        capacity = np.array(capacity).astype(np.float64)
    
    if len(capacity.shape) != 2:
        raise ValueError(f"Expected dim 2 array, got {len(capacity.shape)}!")
    
    r, c = capacity.shape
    if r != c:
        raise ValueError(f"Expected 2d square array, got dimension {r}x{c}")
    
    if s >= r or t >= r:
        raise ValueError(f"Source ({s}) or sink ({t}) exceeded graph size ({r})")
    
    return rsgraphlib.edmonds_karp(capacity, s, t)


def bellman_ford(adj: np.ndarray, source: int) -> Tuple[Dict[int, float], Dict[int, List[int]]]:
    """
    Computes the Edmonds Karp maximum flow algorithm
    
    Args:
        adj (np.ndarray): 2d adjacency matrix
        source (int): source node
        
    Returns:
        Dict[int, float]: shortest distance to each node from source
        Dict[int, List[int]]: shortest path to each node from source
    """
    if not isinstance(adj, np.ndarray):
        adj = np.array(adj).astype(np.float64)
    
    if len(adj.shape) != 2:
        raise ValueError(f"Expected dim 2 array, got {len(adj.shape)}!")
    
    r, c = adj.shape
    if r != c:
        raise ValueError(f"Expected 2d square array, got dimension {r}x{c}")
    
    if source >= r:
        raise ValueError(f"Source ({source}) exceeded graph size ({r})")
    
    distance, path = rsgraphlib.bellman_ford(adj, source)
    
    if len(distance) == 0:
        raise NegativeCycleException("Negative cycle detected.")
    
    return distance, path