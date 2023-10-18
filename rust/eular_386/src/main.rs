use std::collections::HashMap;
use std::time::{Instant};


fn represent_as_primes(primes: &mut [i32; 100000], mut n: i32) -> (i32, std::collections::HashMap<i32, i32>) {
    
    let mut ret:HashMap<i32, i32> = HashMap::new();
    let mut  total:i32 = 0;
    let mut index:usize = 0;

    for p in primes.iter() {
        if  (*p == 0) || (*p > n)   {
            break;
        }
        while n%p == 0 {
            total +=1;
            n = n/p;
            
            if ret.contains_key(p) {
                ret.insert(*p,ret.get(p).unwrap() + 1);
            } else {
                ret.insert(*p,1);
            }

        }
        index += 1;
    }

    if n > 1 {
        primes[index] = n;
        total = 1;
        ret.insert(n,1);
    }

    return (total,ret);
}


fn main() {
    
    let mut start = Instant::now();
    let mut duration = start.elapsed();

    println!("-------------------------------------------------------------- STARTING MAIN " );

    // let mut primes: [i32; 100000000] = [0; 100000000];
    let mut primes: [i32; 100000] = [0; 100000];
    
    
    primes[0] = 2;
    let mut print_threshold = 2;
    let mut s = 0;

    for n in 0..1048577 {
        let x = represent_as_primes(& mut primes,n);
        s += x.0;

        if n % print_threshold == 0 {
            print_threshold = print_threshold * 2;
            
            duration = start.elapsed();
            start = Instant::now();

            println!("{}\t{}\t{:?}", n, s, duration);
            
        }
    }


    duration = start.elapsed();
    println!("\n-------------------------------------------------------------- ALL IS WELL, passed {:?} ",duration );
}
