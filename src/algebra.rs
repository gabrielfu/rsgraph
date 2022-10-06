use ndarray::prelude::*;
use crate::sortarray::{SortArray, PermuteArray};

pub fn normalize(a: &Array1<f64>) -> Array1<f64> {
    let sum = a.iter().map(|x| x * x).sum::<f64>().sqrt();
    a.iter().map(|x| x / sum).collect()
}

pub fn dot(a: &Array1<f64>, b: &Array1<f64>) -> f64 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

pub fn diff(a: &Array1<f64>) -> Array1<f64> {
    a.slice(s![..-1]).iter().zip(a.slice(s![1..])).map(|(x, y)| y - x).collect()
}

pub fn sort(a: &Array1<f64>) -> Array1<f64> {
    let b = a.clone();
    let perm = b.sort_axis_by(Axis(0), |i, j| b[i] < b[j]);
    b.permute_axis(Axis(0), &perm)
}

pub fn bisect_right(a: &Array1<f64>, v: f64) -> usize {
    let mut lo: usize = 0;
    let mut hi: usize = a.len();
    while lo < hi {
        let mid = (lo + hi) / 2;
        if a[mid] <= v {
            lo = mid + 1;
        }
        else {
            hi = mid;
        }
    }
    lo
}

pub fn searchsorted(a: &Array1<f64>, v: &Array1<f64>) -> Array1<usize> {
    v.iter().map(|&i| bisect_right(&a, i)).collect()
}

pub fn cumsum(a: &Array1<f64>) -> Array1<f64> {
    let mut r = a.clone();
    for i in 1..a.len() {
        r[i] = r[i - 1] + r[i];
    }
    r
}