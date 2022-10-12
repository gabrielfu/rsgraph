#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_variables)]

use std::collections::{VecDeque, HashMap};
use crate::structs::graph::{Graph, Node, Edge};
use crate::structs::disjoint_set::DisjointSet;


pub fn kruskal(g: &Graph) -> Vec<Edge>{
    // disjoint set
    let mut subtree = DisjointSet::new();
    for v in g.nodes.iter() {
        subtree.make_set(v);
    }

    // mst
    let mut mst: Vec<Edge> = vec![];

    // sort the edges by ascending weight
    let mut edges = g.edges.clone();
    edges.sort_by(|a, b| a.weight.partial_cmp(&b.weight).unwrap());

    for edge in edges.iter() {
        let Edge { src: u, dest: v, weight: _ } = edge;
        let ru = subtree.find(u);
        let rv = subtree.find(v);
        if ru != rv  {
            mst.push(*edge);
            subtree.union(&ru, &rv);
        }
    }

    mst
}