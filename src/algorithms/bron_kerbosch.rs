use core::panic;
use std::collections::{VecDeque, HashMap, HashSet};
use crate::structs::graph::{Graph, Node, Edge};

pub fn bron_kerbosch(adj_list: &HashMap<Node, HashSet<Node>>, nodes: HashSet<Node>) {
    // let adj_list = _adj_list.clone();
    if adj_list.len() == 0 {
        return;
    }

    // Initialize Q with the given nodes and subg, cand with their nbrs
    let mut sets: Vec<HashSet<i32>> = nodes.iter().map(|node| adj_list.get(node).unwrap().clone()).collect();
    let (cand, others) = sets.split_at_mut(1);
    let cand = &mut cand[0];
    for other in others {
        cand.retain(|e| other.contains(e));
    }
}