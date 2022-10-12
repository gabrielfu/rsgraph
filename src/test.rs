use ndarray::arr2;

use super::*;

#[test]
fn test_edmonds_karp() {
    use ndarray::arr2;

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

    let out = algorithms::edmonds_karp::edmonds_karp(&capacity.view(), s, t);
    assert_eq!(out, 27.);
}

#[test]
fn test_bellman_ford() {
    use crate::graph::Graph;

    // test for no negative cycle
    {
        let adj = arr2(&[
            [13., 10.,  8.,  4.,  4.,  0.],
            [ 1.,  0.,  2., 13., 10., 14.],
            [ 8.,  9., 15., 11., 10.,  8.],
            [ 8., 14.,  4., 13., 10.,  0.],
            [ 6., 13.,  8.,  0., 12., 11.],
            [13.,  2.,  1., 13.,  0.,  8.],
        ]);
        let g = Graph::from_adj_matrix(&adj.view());
        let source = 0;

        let (distance, path) = algorithms::bellman_ford::bellman_ford(&g, source);
        assert_eq!(distance, HashMap::from([
            (0, 0.0), 
            (1, 10.0), 
            (2, 8.0), 
            (3, 4.0), 
            (4, 4.0), 
            (5, 15.0),
        ]));
        assert_eq!(path, HashMap::from([
            (0, vec![0]), 
            (1, vec![0, 1]), 
            (2, vec![0, 2]), 
            (3, vec![0, 3]), 
            (4, vec![0, 4]), 
            (5, vec![0, 4, 5]),
        ]));
    }

    // test for negative cycle
    {
        let adj = arr2(&[
            [ 1.,  0.,  0., -1.],
            [-1., -2., -2., -2.],
            [-2.,  1.,  0.,  1.],
            [ 0.,  0.,  1.,  0.],
        ]);
        let g = Graph::from_adj_matrix(&adj.view());
        let source = 0;

        let (distance, path) = algorithms::bellman_ford::bellman_ford(&g, source);
        assert_eq!(distance, HashMap::from([]));
        assert_eq!(path, HashMap::from([]));
    }
}

#[test]
fn test_graph() {
    use ndarray::arr2;
    use crate::graph::Graph;

    {
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
        let cg = Graph::from_adj_matrix(&(capacity.view()));
        assert_eq!(cg.v, 8);
        assert_eq!(cg.e, 56);
    }
}