pub mod algorithms {

    use ndarray::{Array1, Array2, ArrayView2, Axis};
    use std::collections::VecDeque;

    pub fn edmonds_karp(capacity: &ArrayView2<'_, f64>, s: i32, t: i32) -> f64 {
        let nv: usize = capacity.len_of(Axis(0));
        let mut flow: f64 = 0.;
        let mut residual = Array2::zeros((nv, nv));
        
        // bgf
        loop {
            // let q = arr1(&[s]);
            let mut q: VecDeque<i32> = VecDeque::new();
            q.push_back(s);
            let mut p = Array1::zeros::<usize>(nv);
            p.iter_mut().for_each(|x| *x = -1);
            let mut df = f64::MAX;
            while q.len() > 0 {
                let u = q.pop_front().unwrap();
                for v in 0..nv {
                    let cap: f64 = capacity[[u as usize, v]];
                    let res: f64 = residual[[u as usize, v]];
                    if cap > 0. && cap > res && p[v] < 0 {
                        p[v] = u;
                        let _df = cap - res;
                        if _df < df {
                            df = _df;
                        }
                        if v as i32 != t {
                            q.push_back(v as i32);
                        }
                    }
                }
            }

            if p[t as usize] >= 0 {
                flow += df;
                let mut v = t;
                while v != s {
                    let u = p[v as usize];
                    residual[[u as usize, v as usize]] += df;
                    residual[[v as usize, u as usize]] -= df;
                    v = u;
                }
            }
            else {
                break
            }
        }
        
        flow
    }
}
