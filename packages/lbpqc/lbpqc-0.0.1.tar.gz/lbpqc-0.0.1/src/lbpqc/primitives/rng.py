from lbpqc.type_aliases import *

from lbpqc.primitives.integer.prime import *
from lbpqc.primitives.integer import integer_ring

import random
import math


class RNG:
    def __init__(self, seed) -> None:
        r'''
        Initialize numpy rng with seed value.  
        Use `secrets.randbits(128)` for more cryptographicly secure rng.
        '''
        self._nprng = np.random.default_rng(seed)
        self._pyrng = random.Random(seed)
        
        
    
    @property
    def rng(self):
        r'''
        Access the underlying `numpy` rng object.

        Args:

        Returns:
    
        '''
        return self._nprng
    
    
    def sample_rounded_gaussian(self, q, alpha, size = None) -> int | VectorInt | MatrixInt:
        return np.rint(self.rng.normal(0, (q * alpha) / (2 * np.pi), size)).astype(int)
    

    def sample_discrete_gaussian(self, s: float, c: float, n: int, k: int = 100) -> int:
        r'''
        *How to Use a Short Basis: Trapdoors for Hard Lattices and New Cryptographic Constructions; page 14; 4.1 Sampling Integers;*

        Args:

        Returns:
    
        '''
        gaussian = lambda x, s, c: np.exp((-np.pi * np.dot(x - c, x - c)) / (s * s))
        t = np.log(n)
        a = int(np.ceil(c - s * t))
        b = int(np.floor(c + s * t))
        for _ in range(k * int(np.ceil(t))):
            x = self.rng.integers(a, b, endpoint=True)
            if self.rng.random() < gaussian(x, s, c):
                return x

        raise RuntimeError("This shouldn't happen")
    

    def sample_uniform_Zq(self, q: int, size : None | int | Tuple[int,int] = None) -> ModInt | VectorModInt | MatrixModInt:
        r'''
        Sample uniformly from $\mathbb{Z}_{q}$ ring.  
        If size is None, returns single element.  
        If size is an int, returns vector (1 dim np.ndarray) with given size.  
        If size is a tuple, returns matrix (2 dim np.ndarray) with given shape.

        Args:

        Returns:
    
        '''
        return self.rng.integers(0, q, size)
    

    def _get_dist(self, name: str, *args):
        match name:
            case 'rounded':
                return self.sample_rounded_gaussian(*args)
            case 'discrete':
                return self.sample_discrete_gaussian(*args)

        raise ValueError(f"Unknown distribution {name}")
    

    def LWE_dist(self, q: int, s: VectorInt, m: int, err_dist: str, *args) -> Tuple[MatrixModInt, VectorInt]:
        r'''

        Args:

        Returns:
    
        '''
        n = s.shape[0]
    
        e = np.array([self._get_dist(err_dist, *args) for _ in range(m)])
        A = self.sample_uniform_Zq(q, (m, n))
        b = A @ s + e
        return A, b
    
    
    def row_LWE_dist(self, q: int, s: VectorInt, err_dist: str, *args) -> Tuple[VectorInt, int]:
        r'''

        Args:

        Returns:
    
        '''
        n = s.shape[0]
        e = self._get_dist(err_dist, *args)
        a = self.sample_uniform_Zq(q, n)
        b = np.dot(a, s)
        return a, b
    

    def LWR_dist(self, q: int, p: int, s: VectorInt, m :int) -> Tuple[MatrixModInt, VectorModInt]:
        r'''

        Args:

        Returns:
    
        '''
        n = s.shape[0]
        A = self.sample_uniform_Zq(q, (m, n))
        b = integer_ring.LWR_rounding(A @ s, q, p)
        return A, b
    

    def row_LWR_dist(self, q: int, p: int, s: VectorInt) -> Tuple[VectorInt, ModInt]:
        r'''

        Args:

        Returns:
    
        '''
        n = s.shape[0]
        a = self.sample_uniform_Zq(q, n)
        b = integer_ring.LWR_rounding(np.dot(a, s), q, p)
        return a, b


    def sample_Zq_subset(self, q: int) -> VectorModInt:
        r'''

        Args:

        Returns:
    
        '''
        subset_size = self.rng.integers(0, q)
        return self.rng.choice(q, subset_size, replace=False)
    

    def sample_prime(self, a: int, b: int = None):
        r'''
        samples a random prime from interval [a, b)
        number of primes in interval $(0, x]$ - $\pi(x) \approx \frac{x}{\log{x}}$
        so number of primes in [a, b) is approximetly equal to $P = \frac{b}{\log{b}} - \frac{a}{\log{a}}$.
        probabiliy of uniformly chosen integer from (a,b] being a prime - $p = \frac{P}{b - a}$

        P(not getting prime) = 1 - p
        P(not getting any prime in n trials) = (1 - p)^n
        P(getting at least one prime in n trials) = 1 - (1 - p)^n
        0.99 = 1 - (1 - p)^n
        (1 - p)^n = 0.01
        n = log(0.01, 1 - p)
        n = ln(0.01)/ln(1 - p)

        So in order to be 99% sure that some prime number was sampled, we need to perform n trials
        where n = ln(0.01)/ln(1 - p)

        Args:

        Returns:
    
        '''
        if b is None:
            b = a
            a = 0

        if b <= a:
            raise ValueError(f"[{a}, {b}) is not a proper interval")
        
        if b <= 0:
            raise ValueError(f"there are no prime numbers in interval [{a}, {b})")
        
        if a < 0:
            a = 0

        bigint_log = lambda n, b: int((n.bit_length() - 1) // math.log2(b))
        
        
    
        approx_number_of_primes = b // (math.log(b) if b.bit_length() < 512 else bigint_log(b, math.e))
        if a != 0:
            approx_number_of_primes -= a // (math.log(a) if a.bit_length() < 512 else bigint_log(a, math.e))
        is_prime_probability = approx_number_of_primes / (b - a)

        number_of_samples = int(math.log(0.01) / math.log(1 - is_prime_probability)) + 1

        int_gen = (lambda a,b: self.rng.integers(a,b)) if b < 2 ** 63 - 1 else (lambda a,b: self._pyrng.randint(a, b - 1))

        for _ in range(number_of_samples):
            prime_candidate = int_gen(a,b)
            if miller_rabin_primality_test(prime_candidate, 15, int_gen):
                return prime_candidate
        
        raise ValueError("exceeded maximum number of trials for sampling a prime from [a, b)")


    def sample_kbits_prime(self, kbits: int):
        r'''

        Args:

        Returns:
    
        '''
        a = 2**(kbits - 1)
        b = 2**kbits
        return self.sample_prime(a, b)



