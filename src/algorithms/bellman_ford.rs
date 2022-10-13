use std::collections::{VecDeque, HashMap};
use crate::structs::graph::{Graph, Node, Edge};

pub fn _bellman_ford(g: &Graph, src: Node) -> (bool, HashMap<Node, f64>, HashMap<Node, Node>) {
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
            // detected negative cycle
            return (true, dist, parents);
        }
    }

    // did not detect any negative cycle
    return (false, dist, parents);
}

pub fn bellman_ford(g: &Graph, src: Node) -> (HashMap<Node, f64>, HashMap<Node, Vec<Node>>) {
    let mut distance: HashMap<Node, f64> = HashMap::new();
    let mut path: HashMap<Node, Vec<Node>> = HashMap::new();

    let (neg_cycle, dist, parents) = _bellman_ford(g, src);
    if !neg_cycle {
        distance = dist;
        for node in g.nodes.iter() {
            let mut node_path: VecDeque<Node> = VecDeque::new();
            let mut p = node;
            loop {
                node_path.push_front(*p);
                if *p == src {
                    break
                }
                p = parents.get(p).unwrap();
            }
            path.insert(*node, Vec::from(node_path));
        }
    }

    return (distance, path);
}