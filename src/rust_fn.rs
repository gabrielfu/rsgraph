use ndarray::{Array1, Array2, ArrayView2, Axis};
use std::collections::{VecDeque, HashMap};
use crate::graph::{Graph, Node, Edge};

pub mod algorithms {
    use super::*;

    pub fn edmonds_karp(capacity: &ArrayView2<'_, f64>, s: usize, t: usize) -> f64 {
        let nv: usize = capacity.len_of(Axis(0));
        let mut flow: f64 = 0.;
        let mut residual = Array2::zeros((nv, nv));
        
        loop {
            // BFS
            // BFS queue
            let mut q: VecDeque<usize> = VecDeque::new();
            q.push_back(s);
            // parent vertex in shortest path
            // initialize to `nv` to represent null
            let mut p = Array1::zeros::<usize>(nv);
            p.iter_mut().for_each(|x| *x = nv);
            let mut df = f64::MAX;
            while q.len() > 0 {
                let u = q.pop_front().unwrap();
                for v in 0..nv {
                    let cap: f64 = capacity[[u, v]];
                    let res: f64 = residual[[u, v]];
                    if cap > 0. && cap > res && p[v] == nv {
                        p[v] = u;
                        let _df = cap - res;
                        if _df < df {
                            df = _df;
                        }
                        if v != t {
                            q.push_back(v);
                        }
                    }
                }
            }

            if p[t] < nv {
                flow += df;
                let mut v = t;
                while v != s {
                    let u = p[v];
                    residual[[u, v]] += df;
                    residual[[v, u]] -= df;
                    v = u;
                }
            }
            else {
                break
            }
        }
        
        flow
    }

    
    pub fn bellman_ford(g: &Graph, src: Node) -> bool {
        // init
        let mut dist: HashMap<Node, f64> = HashMap::new();
        let mut parents: HashMap<Node, Node> = HashMap::new();
        for v in g.nodes.iter() {
            dist.insert(*v, f64::MAX);
            parents.insert(*v, -1);
        }

        // distance to src is 0
        dist.insert(src, 0.);
        
        // relax edges for |V| - 1 times
        for _ in 0..(g.v - 1) {
            for edge in g.edges.iter() {
                let Edge { src: u, dest: v, weight: w} = edge;
                let du = *(dist.get(u).unwrap());
                let dv = *(dist.get(v).unwrap());
                if du != f64::MAX && du + *w < dv {
                    dist.insert(*v, du + *w);
                    parents.insert(*v, *u);
                }
            }
        }

        // check for negative weight cycles
        for edge in g.edges.iter() {
            let Edge { src: u, dest: v, weight: w} = edge;
            let du = *(dist.get(u).unwrap());
            let dv = *(dist.get(v).unwrap());
            if du != f64::MAX && du + *w < dv {
                return true;
            }
        }

        return false;
    }
}
