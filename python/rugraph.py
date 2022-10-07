import os
os.environ["RUST_BACKTRACE"] = "full"
import rugraphlib as lib
import numpy as np

def edmonds_karp(capacity: np.ndarray, s: int, t: int) -> float:
    """
    asdsa
    
    Args:
        capacity (np.ndarray): 2-d grid
        s (int): source node
        t (int): sink node
        
    Returns:
        float: maximum flow
    """
    if not isinstance(capacity, np.ndarray):
        capacity = np.array(capacity)
    
    if len(capacity.shape) != 2:
        raise ValueError(f"Expected dim 2 array, got {len(capacity.shape)}!")
    
    r, c = capacity.shape
    if r != c:
        raise ValueError(f"Expected square 2d array, got {r}x{c}")
    
    if s >= r or t >= r:
        raise ValueError(f"Source ({s}) or sink ({t}) exceeded path size ({r})")
    
    return lib.edmonds_karp(capacity, s, t)