//! A simplistic implementation of graph objects
//! supporting weighted and directed edges

use ndarray::{ArrayView2, Axis};
use std::collections::{HashSet};

/// Represents node ID
pub type Node = i32;

/// Represents a weighted directed edge from a source to a destination
#[derive(Clone, Debug)]
pub struct Edge {
    pub src: Node,
    pub dest: Node,
    pub weight: f64,
}

impl Edge {
    pub fn unweighted_edge(src: Node, dest: Node) -> Edge {
        Edge { src, dest, weight: 1. }
    }

    pub fn weighted_edge(src: Node, dest: Node, weight: f64) -> Edge {
        Edge { src, dest, weight }
    }
}

/// Represents a graph object
#[derive(Clone, Debug)]
pub struct Graph {
    pub v: usize, // num vertices
    pub e: usize, // num edges
    pub nodes: HashSet<Node>,
    pub edges: Vec<Edge>,
}

impl Graph {
    /// Construct an empty Graph object
    pub fn new() -> Graph {
        Graph { v: 0, e: 0, nodes: HashSet::new(), edges: vec![]}
    }

    pub fn clone(&mut self) -> Graph {
        let mut g = Graph::new();
        g.nodes = self.nodes.clone();
        g.edges = self.edges.clone();
        g.v = self.v;
        g.e = self.e;
        return g;
    }

    /// Construct a new Graph object from an `ndarray` adjacency matrix
    pub fn from_adj_matrix(adj: &ArrayView2<f64>) -> Graph {
        let mut g = Graph::new();
        let n = adj.len_of(Axis(0));

        for i in 0..n {
            for j in 0..n {
                let value = adj[[i, j]];
                if value != 0. {
                    g.add_weighted_edge(i as Node, j as Node, value);
                }
            }
        }
        g
    }

    fn add_node(&mut self, node: Node) {
        if !self.nodes.contains(&node) {
            self.nodes.insert(node);
            self.v += 1;
        }
    }

    /// Add an unweighted directed edge
    pub fn add_unweighted_edge(&mut self, src: Node, dest: Node) {
        self.add_weighted_edge(src, dest, 1.);
    }

    /// Add a weighted directed edge
    pub fn add_weighted_edge(&mut self, src: Node, dest: Node, weight: f64) {
        self.add_node(src);
        self.add_node(dest);
        self.edges.push(Edge::weighted_edge(src, dest, weight));
        self.e += 1;
    }
}

