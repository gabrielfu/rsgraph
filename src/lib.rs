use pyo3::prelude::*;
use numpy::{PyReadonlyArray1, PyArray1};
use wasserstein::wasserstein;
mod sortarray;
mod algebra;
mod wasserstein;

/// Computes the Wasserstein distance
#[pyfunction]
fn wasserstein_distance<'py>(
    u_values: PyReadonlyArray1<f64>,
    v_values: PyReadonlyArray1<f64>,
    u_weights: Option<PyReadonlyArray1<f64>>,
    v_weights: Option<PyReadonlyArray1<f64>>,
) -> f64 {
    let u_values = u_values.as_array().to_owned();
    let v_values = v_values.as_array().to_owned();
    let u_weights = match u_weights {
        Some(pyarr) => Some(pyarr.as_array().to_owned()),
        None => None,
    };
    let v_weights = match v_weights {
        Some(pyarr) => Some(pyarr.as_array().to_owned()),
        None => None,
    };
    wasserstein(&u_values, &v_values, u_weights, v_weights)
}


/// A Python module implemented in Rust.
#[pymodule]
fn rust_emd(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(wasserstein_distance, m)?)?;
    Ok(())
}