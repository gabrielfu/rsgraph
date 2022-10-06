use ndarray::prelude::*;
use crate::sortarray::{SortArray, PermuteArray};
use crate::algebra;

pub fn wasserstein(
    u_values: &Array1<f64>, 
    v_values: &Array1<f64>, 
    u_weights: Option<Array1<f64>>,
    v_weights: Option<Array1<f64>>,
) -> f64 {
    let u_sorter = u_values.sort_axis_by(Axis(0), |i, j| u_values[i] < u_values[j]);
    let v_sorter = v_values.sort_axis_by(Axis(0), |i, j| v_values[i] < v_values[j]);

    let mut all_values = u_values.clone();
    all_values.append(Axis(0), v_values.view()).unwrap();
    all_values = algebra::sort(&all_values);

    let deltas = algebra::diff(&all_values);
    println!("all_values: {}", all_values);
    println!("deltas: {}", deltas);

    let to_insert = all_values.slice(s![..-1]).to_owned();
    let u_sorted = u_values.clone().permute_axis(Axis(0), &u_sorter);
    let u_cdf_indices = algebra::searchsorted(&u_sorted, &to_insert);
    let v_sorted = v_values.clone().permute_axis(Axis(0), &v_sorter);
    let v_cdf_indices = algebra::searchsorted(&v_sorted, &to_insert);
    println!("u_cdf_indices: {}", u_cdf_indices);
    println!("v_cdf_indices: {}", v_cdf_indices);


    let u_cdf: Array1<f64> = match u_weights {
        Some(arr) => {
            let mut u_sorted_cumweights = arr1(&[0.]);
            let uw = arr.clone().permute_axis(Axis(0), &u_sorter);
            u_sorted_cumweights.append(Axis(0), algebra::cumsum(&uw).view()).unwrap();
            let u_cdf: Array1<f64> = u_cdf_indices.iter().map(|&i| u_sorted_cumweights[i]).collect();
            let denom = u_sorted_cumweights[u_sorted_cumweights.len() - 1];
            u_cdf.iter().map(|x| x / denom).collect()
        },
        None => {
            u_cdf_indices.iter().map(|&x| x as f64 / u_values.len() as f64).collect()
        },
    };
    let v_cdf: Array1<f64> = match v_weights {
        Some(arr) => {
            let mut v_sorted_cumweights = arr1(&[0.]);
            let vw = arr.clone().permute_axis(Axis(0), &v_sorter);
            v_sorted_cumweights.append(Axis(0), algebra::cumsum(&vw).view()).unwrap();
            let v_cdf: Array1<f64> = v_cdf_indices.iter().map(|&i| v_sorted_cumweights[i]).collect();
            let denom = v_sorted_cumweights[v_sorted_cumweights.len() - 1];
            v_cdf.iter().map(|x| x / denom).collect()
        },
        None => {
            v_cdf_indices.iter().map(|&x| x as f64 / v_values.len() as f64).collect()
        },
    };
    println!("u_cdf: {}", u_cdf);
    println!("v_cdf: {}", v_cdf);

    let abs_diff: Array1<f64> = u_cdf.iter().zip(v_cdf).map(|(&x, y)| (x - y).abs()).collect();
    abs_diff.iter().zip(deltas).map(|(x, y)| x * y).sum()
}


fn main() {
    // array
    {
        let a = arr1(&[5., 2., 7., 1., 9.]);
        let b = arr1(&[2., 3., 5., 0., 4.]);
        println!("a: {}", a);
        println!("b: {}", b);

        let uw = arr1(&[1., 2., 3., 4., 5.]);
        let vw = arr1(&[1., 2., 3., 4., 5.]);
        let dist = wasserstein(&a, &b, Some(uw), Some(vw));
        println!("dist: {}", dist);

        // let c = algebra::cumsum(&a);
        // println!("c: {}", c);

    }
}
