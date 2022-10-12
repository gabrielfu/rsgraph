#![allow(dead_code)]
#![allow(unused_imports)]
#![allow(unused_variables)]

use std::collections::{VecDeque, HashMap};
use crate::structs::graph::{Graph, Node, Edge};


pub fn kruskal(_g: &Graph) -> Graph {

    // avoid mutating the borrowed Graph
    let mut g = (*_g).clone();
    g.edges.sort_by(|a, b| a.weight.partial_cmp(&b.weight).unwrap());

    return g;
}