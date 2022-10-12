use std::collections::HashMap;
use std::cell::RefCell;
use crate::structs::graph::Node;

pub struct DisjointSet {
    pub nodes: Vec<Node>,
    pub parents: RefCell<HashMap<Node, Node>>,
}

impl DisjointSet {
    pub fn new() -> DisjointSet {
        DisjointSet { nodes: vec![], parents: RefCell::new(HashMap::new()) }
    }

    fn get_parent(&self, item: &Node) -> Node {
        let ps = self.parents.borrow_mut();
        let p = ps.get(item).unwrap();
        *p
    }
    
    fn set_parent(&self, item: &Node, parent: &Node) {
        self.parents.borrow_mut().insert(*item, *parent);
    }

    pub fn find(&mut self, item: &Node) -> Node {
        let mut root = *item;
        
        loop {
            let p = self.get_parent(&root);
            if p == root {
                break
            }
            root = p;
        }

        let mut x = *item;
        loop {
            let p = self.get_parent(&x);
            if p == root {
                break
            }
            self.set_parent(&x, &root);
            x = p;
        }

        root
    }

    pub fn union(&mut self, x1: &Node, x2: &Node) {
        let root1 = self.find(x1);
        let root2 = self.find(x2);
        self.set_parent(&root1, &root2);
    }
}