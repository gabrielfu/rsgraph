import os
os.environ["RUST_BACKTRACE"] = "full"
import rugraphlib as lib
import numpy as np

def edmond_karp(path: np.ndarray, s: int, t: int) -> float:
    """
    asdsa
    
    Args:
        path (np.ndarray): 2-d grid
        s (int): source node
        t (int): sink node
        
    Returns:
        float: maximum flow
    """
    if len(path.shape) != 2:
        raise ValueError(f"Expected dim 2 array, got {len(path.shape)}!")
    
    r, c = path.shape
    if r != c:
        raise ValueError(f"Expected square 2d array, got {r}x{c}")
    
    if s >= r or t >= r:
        raise ValueError(f"Source ({s}) or sink ({t}) exceeded path size ({r})")
    
    return lib.edmond_karp(path, s, t)