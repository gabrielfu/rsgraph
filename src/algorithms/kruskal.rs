#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_variables)]

use std::collections::{VecDeque, HashMap};
use crate::structs::graph::{Graph, Node, Edge};
use crate::structs::disjoint_set::DisjointSet;


pub fn kruskal(g: &Graph) -> Graph {
    // disjoint set
    let mut subtree = DisjointSet::new();
    for v in g.nodes.iter() {
        subtree.make_set(v);
    }

    // mst graph
    let mut mst = Graph::new();

    // sort the edges by ascending weight
    let mut edges = g.edges.clone();
    edges.sort_by(|a, b| a.weight.partial_cmp(&b.weight).unwrap());

    for edge in edges.into_iter() {
        let Edge { src: u, dest: v, weight: w } = edge;
        let ru = subtree.find(&u);
        let rv = subtree.find(&v);
        if ru != rv  {
            mst.add_weighted_edge(u, v, w);
            subtree.union(&ru, &rv);
        }
    }

    mst
}