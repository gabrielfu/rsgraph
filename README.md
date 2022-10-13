# rsgraph
Python wrapper API of Rust implementation of common graph algorithms

This package is orders of magnitude faster than pure Python implementation, 
and is up to 10x faster than `networkx` for small graph (size < 100).

## Algorithms
- [Edmonds-Karp maximum flow](https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm)
- [Bellman-Ford shortest path](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm)
- [Kruskal minimum spanning tree](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)

## Prerequisites
- Rust >= 1.56
- Python >= 3.7

## Installation
You can install the package `rsgraph` using pip or by building from source.

### Using pip
```shell
$ pip install git+https://github.com/gabrielfu/rust-graph-algorithms.git
```

### Build from source
1. Clone this repository
    ```shell
    $ git clone https://github.com/gabrielfu/rust-graph-algorithms.git
    $ cd rust-graph-algorithms
    ```

2. Create virtual environment
    ```shell
    $ python -m venv ./venv
    $ source ./venv/bin/activate
    ```

3. Install Python libraries
    ```shell
    $ pip install -r requirements.txt
    ```

4. Build package
    ```shell
    $ python setup.py install
    ```
    Note: if you run `python setup.py develop`, a much slower debug version will be built.


## Examples
### Edmonds-Karp
```python
import rsgraph
import numpy as np

capacity = np.array([
    [0, 1, 0],
    [0, 0, 1],
    [0, 0, 0],
]).astype(np.float64)
s = 0
t = 2
flow = rsgraph.edmonds_karp(capacity, s, t)
print(flow)
```
Output:
```python
1.0
```

### Bellman-Ford
```python
import rsgraph
import numpy as np

adj = np.array([
    [ 0, 10,  8,  4],
    [ 4,  0,  0,  0],
    [ 0, 13,  0, 14],
    [ 8,  9, 15,  0],
]).astype(np.float64)
source = 0
distance, path = rsgraph.bellman_ford(adj, source)
print(distance)
print(path)
```
Output:
```python
{3: 4.0, 0: 0.0, 2: 8.0, 1: 10.0}
{2: [0, 2], 3: [0, 3], 1: [0, 1], 0: [0]}
```

### Kruskal
```python
import rsgraph
import numpy as np

adj = np.array([
    [0, 4, 2, 0, 0, 0],
    [4, 0, 1, 8, 0, 0],
    [2, 1, 0, 0, 4, 0],
    [0, 8, 0, 0, 2, 1],
    [0, 0, 4, 2, 0, 7],
    [0, 0, 0, 1, 7, 0],
]).astype(np.float64)
mst = rsgraph.kruskal(adj)
print(mst)
```
Output:
```python
[[0. 0. 2. 0. 0. 0.]
 [0. 0. 1. 0. 0. 0.]
 [2. 1. 0. 0. 4. 0.]
 [0. 0. 0. 0. 2. 1.]
 [0. 0. 4. 2. 0. 0.]
 [0. 0. 0. 1. 0. 0.]]
```

## Benchmarking
1. Install Python libraries
    ```shell
    $ pip install -r ./benchmark/requirements.txt
    ```

2. Run 
    ```shell
    $ python ./benchmark/main.py
    ```

### Edmonds-Karp
Benchmarking against `networkx` (nx) and pure Python implementation:
```
Benchmarking: Edmonds-Karp
Graph size: 32
nx_flow: 50 loops, best of 5: 4.33 msec per loop
nx_ek: 100 loops, best of 5: 3.33 msec per loop
python: 5 loops, best of 5: 59.3 msec per loop
rust: 500 loops, best of 5: 406 usec per loop
```

Using `perfplot`:
![](./images/perf_edmonds_karp.png)

### Bellman-Ford
Benchmarking against `networkx` (nx) and Pure python implementation:
```
Benchmarking: Bellman-Ford
Graph size: 32
nx_bf: 200 loops, best of 5: 1.76 msec per loop
python: 20 loops, best of 5: 15.7 msec per loop
rust: 500 loops, best of 5: 786 usec per loop
```

Using `perfplot`:
![](./images/perf_bellman_ford.png)

### Kruskal
Benchmarking against `networkx` (nx):
```
Benchmarking: Kruskal
Graph size: 32
nx: 100 loops, best of 5: 2.35 msec per loop
rust: 2000 loops, best of 5: 154 usec per loop
```
