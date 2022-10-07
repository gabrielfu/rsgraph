import rsgraphlib
import numpy as np

def edmonds_karp(capacity: np.ndarray, s: int, t: int) -> float:
    """
    Computes the Edmonds Karp maximum flow algorithm
    
    Args:
        capacity (np.ndarray): 2d array
        s (int): source vertex
        t (int): sink vertex
        
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