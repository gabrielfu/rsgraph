use std::collections::HashMap;
use numpy::{PyReadonlyArray2, PyArray2};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

mod algorithms;
mod structs;
use structs::graph::{Graph, Node};

#[pymodule]
fn rsgraphlib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn edmonds_karp<'py>(_py: Python<'_>, x: PyReadonlyArray2<f64>, s: usize, t: usize) -> f64 {
        let array = x.as_array();
        algorithms::edmonds_karp::edmonds_karp(&array, s, t)
    }

    #[pyfn(m)]
    fn bellman_ford<'py>(_py: Python<'_>, x: PyReadonlyArray2<f64>, source: Node) -> (HashMap<Node, f64>, HashMap<Node, Vec<Node>>) {
        let array = x.as_array();
        let g = Graph::from_adj_matrix(&array);
        algorithms::bellman_ford::bellman_ford(&g, source)
    }

    #[pyfn(m)]
    fn kruskal<'py>(_py: Python<'py>, x: PyReadonlyArray2<f64>) -> &'py PyArray2<f64> {
        let array = x.as_array();
        let g = Graph::from_adj_matrix(&array);
        let mst = algorithms::kruskal::kruskal(&g);
        let mst_adj = mst.to_adj_matrix();
        let mst_array = PyArray2::from_array(_py, &mst_adj);
        mst_array
    }

    Ok(())
}

#[cfg(test)]
mod test;