use std::collections::HashMap;
use numpy::PyReadonlyArray2;
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

// mod rust_fn;
// use rust_fn::algorithms;

mod graph;
use graph::{Graph, Node};

mod algorithms;

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

    Ok(())
}

#[cfg(test)]
mod test;