use numpy::{PyReadonlyArray2};
use pyo3::prelude::{pymodule, PyModule, PyResult, Python};

mod rust_fn;
use rust_fn::algorithms;

#[pymodule]
fn rugraphlib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    #[pyfn(m)]
    fn edmonds_karp<'py>(_py: Python<'_>, x: PyReadonlyArray2<f64>, s: i32, t: i32) -> f64 {
        let array = x.as_array();
        algorithms::edmonds_karp(&array, s, t)
    }

    Ok(())
}


#[cfg(test)]
mod test {
    use super::*;
    use ndarray::arr2;

    #[test]
    fn test_edmonds_karp() {
        let capacity = arr2(&[
            [13., 10.,  8.,  4.,  4.,  0.,  1.,  0.],
            [ 2., 13., 10., 14.,  8.,  9., 15., 11.],
            [10.,  8.,  8., 14.,  4., 13., 10.,  0.],
            [ 6., 13.,  8.,  0., 12., 11., 13.,  2.],
            [ 1., 13.,  0.,  8.,  1.,  4.,  7.,  6.],
            [ 6.,  0.,  0.,  1.,  0., 10.,  8., 10.],
            [ 4.,  9., 12.,  6.,  7., 15., 12., 15.],
            [ 6., 10., 15., 10., 13., 11., 11.,  6.],
        ]);
        let s = 0;
        let t = 7;

        let out = algorithms::edmonds_karp(&capacity.view(), s, t);
        assert_eq!(out, 27.);
    }
}
