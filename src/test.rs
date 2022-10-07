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

    let out = algorithms::edmonds_karp(&capacity.view(), s, t);
    assert_eq!(out, 27.);
}

#[test]
fn test_bellman_ford() {
    use crate::graph::Graph;

    {
        let mut g = Graph::new();
        g.add_weighted_edge(0, 1, 2.);
        g.add_weighted_edge(1, 2, 1.);
        g.add_weighted_edge(2, 0, -2.);

        let neg = algorithms::bellman_ford(&g, 1);
        assert_eq!(neg, false);
    }

    {
        let mut g = Graph::new();
        g.add_weighted_edge(0, 1, 2.);
        g.add_weighted_edge(1, 2, 1.);
        g.add_weighted_edge(2, 0, -5.);

        let neg = algorithms::bellman_ford(&g, 1);
        assert_eq!(neg, true);
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