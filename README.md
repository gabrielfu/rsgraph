# rugraph
Rust implementation of common graph algorithms with Python binding

## Algorithms
- Edmonds-Karp maximum flow

## Prerequisites
- rust 2021
- python >= 3.7

## Usage
### Build from source
1. Create virtual environment
    ```shell
    python -m venv ./venv
    ./venv/Scripts/activate
    ```

2. Install maturin
    ```shell
    pip install maturin
    ```

3. Build rust package in python
    ```shell
    maturin develop --release
    ```

4. Import in python
    ```python
    import rugraph
    ```

## Examples
### Edmonds-Karp
```python
import rugraph
import numpy as np

capacity = np.array([
    [0, 1, 0],
    [0, 0 ,1],
    [0, 0, 0],
]).astype(np.float64)
s = 0
t = 2
flow = rugraph.edmonds_karp(capacity, s, t)
print(flow)
```
Output:
```python
1.0
```

## Benchmarking
Run 
```python
python ./python/main.py
```

### Edmond-Karps
```
Benchmarking: Edmonds-Karp
Validating output: nx_flow=138.0, nx_ek=138.0, python=138.0, rust=138.0
nx_flow: 100 loops, best of 5: 3.97 msec per loop
nx_ek: 50 loops, best of 5: 3.24 msec per loop
python: 5 loops, best of 5: 41.8 msec per loop
rust: 1000 loops, best of 5: 266 usec per loop
```