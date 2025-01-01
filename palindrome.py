"""
Module for palindrome related functions and classes.

ITERATORS:
- `square_divisors`: Iterate over the divisors of n^2.
- `palindrome_divisors`: Iterate over the palindromic divisors of a number.
- `farey_sequence`: Iterate over all reduced fractions with denominator <=n.

- `pal_iterator_`: Iterate over palindromic integers with a given number of digits.
- `pal_iterator`: Iterate over palindromic integers in a range.
- `pal_div_iterator`: Iterate over palindromic integers in a range that is a multiple
                        of a given divisor.

- `reciprocal_pair_iterator`: Iterate over solutions to $p/q=1/a+1/b$.
- `reciprocal_pair_iterator_r`: Iterate over solutions to $r=1/a+1/b$.
- `reciprocal_pal_pair_iterator`: Iterate over palindromic solutions to $p/q=1/a+1/b$.
- `reciprocal_pal_pair_iterator_r`: Iterate over palindromic solutions to $r=1/a+1/b$.
- `egyptian_pair_iterator`: Iterate over solutions to $p/q=1/a+1/b$ with a<b.
- `egyptian_pair_iterator_r`: Iterate over solutions to $r=1/a+1/b$ with a<b.
- `egyptian_pal_pair_iterator`: Iterate over palindromic solutions to $p/q=1/a+1/b$ with a<b.
- `egyptian_pal_pair_iterator_r`: Iterate over palindromic solutions to $r=1/a+1/b$ with a<b.
- `reciprocal_iterator`: Iterate over solutions to $p/q=1/p_1+1/p_2+...+1/p_k$.
- `reciprocal_iterator_r`: Iterate over solutions to $r=1/p_1+1/p_2+...+1/p_k$.
- `egyptian_iterator`: Iterate over solutions to $p/q=1/p_1+1/p_2+...+1/p_k$ 
                       with $p_1<p_2<...<p_k$.
- `egyptian_iterator_r`: Iterate over solutions to $r=1/p_1+1/p_2+...+1/p_k$ 
                         with $p_1<p_2<...<p_k$.
- `reciprocal_pal_iterator`: Iterate over palindromic solutions to 
                             $p/q=1/p_1+1/p_2+...+1/p_k$.
- `reciprocal_pal_iterator_r`: Iterate over palindromic solutions to 
                               $r=1/p_1+1/p_2+...+1/p_k$.
- `egyptian_pal_iterator`: Iterate over palindromic solutions to
                            $p/q=1/p_1+1/p_2+...+1/p_k$ with $p_1<p_2<...<p_k$.
- `egyptian_pal_iterator_r`: Iterate over palindromic solutions to
                              $r=1/p_1+1/p_2+...+1/p_k$ with $p_1<p_2<...<p_k$.

SOLVERS:

HELPER FUNCTIONS:
- `pal_floor`: Find the largest palindromic number less than or equal to a number.
- `prev_pal`: Find the largest palindromic number less than a number.
- `pal_ceil`: Find the smallest palindromic number greater than or equal to a number.
- `next_pal`: Find the smallest palindromic number greater than a number.
"""
import sympy
from sympy import factorint, Rational
from sympy.ntheory import is_palindromic
import itertools
from typing import List, Tuple, Iterator

def pal_floor(n: int) -> int:
    """
    Find the largest palindromic number <= n.
    USAGE:  `pal = pal_floor(n)`
    """
    assert(n>=0)
    if n>0 and n%10 == 0:
        n-=1
    s = str(n)
    if len(s)<=1:
        return(n)
    l = len(s)//2
    is_odd = len(s)%2
    s1 = s[:l+is_odd]
    s1_rev = s1[-1::-1]
    s2 = s[-(l+is_odd)::]
    if (int(s1_rev)<=int(s2)):
        return(int(s1+s1_rev[is_odd::]))
    else:
        s1 = str(int(s1)-1)
        s2 = s1[-1::-1]
        return(int(s1+s2[is_odd::]))

def prev_pal(n: int) -> int:
    """
    Return the largest palindrome <n.
    USAGE:  `pal = prev_pal(n)`
    """
    if is_palindromic(n):
        return(pal_floor(n-1))
    else:
        return(pal_floor(n))


def pal_ceil(n: int) -> int:
    """
    Find the smallest palindromic number >=n.
    USAGE:  `pal = pal_ceil(n)`
    """
    assert(n>=0)
    s = str(n)
    if len(s)<=1:
        return(n)
    l = len(s)//2
    is_odd = len(s)%2
    s1 = s[:l+is_odd]
    s1_rev = s1[-1::-1]
    s2 = s[-(l+is_odd)::]
    if (int(s1_rev)>=int(s2)):
        return(int(s1+s1_rev[is_odd::]))
    else:
        s1 = str(int(s1)+1)
        s2 = s1[-1::-1]
        return(int(s1+s2[is_odd::]))

def next_pal(n: int) -> int:
    """
    Return the largest palindrome >n.
    USAGE:  `pal = next_pal(n)`
    """
    if is_palindromic(n):
        return(pal_ceil(n+1))
    else:
        return(pal_ceil(n))
    
    
def palindrome_divisors(n: int, min_value: int=1) -> Iterator[int]:
    """
    Return the palindromic divisors of n that are larger than min_value.
    USAGE: `for i in palindrome_divisors(n, min_value):`
    """
    for i in sympy.divisors(n):
        if is_palindromic(i) and i>min_value:
            yield i


def square_divisors(n: int, proper:bool=False)->Iterator[int]:
    """Helper function for divisors which generates the divisors of n^2."""

    factordict = factorint(n)
    for i in factordict:
        factordict[i] = factordict[i]*2
    ps = sorted(factordict.keys())

    def rec_gen(n=0):
        if n == len(ps):
            yield 1
        else:
            pows = [1]
            for j in range(factordict[ps[n]]):
                pows.append(pows[-1] * ps[n])
            for q in rec_gen(n + 1):
                for p in pows:
                    yield p * q
    if proper:
        for p in rec_gen():
            if p != n:
                yield p
    else:
        yield from rec_gen()


def farey_sequence(n: int, small_only: bool = False, omit_zero: bool = True) -> Iterator[Rational]:
    """
    Generate all reduced fractions a/b with 0<=a<=b<=n according to the Farey 
    sequence algorithm.
    If small_only is True, only fractions with a<=b are generated.
    USAGE:  `for r in farey_sequence(n):`
    """
    a, b, c, d = 0, 1, 1, n
    # skipping 0 as it is not interesting
    if not omit_zero:
        yield Rational(a,b)
    while 0 <= c <= n:
        k = (n + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield Rational(a, b)
    if not small_only:
        a, c = 1, n - 1
        while 0 <= c <= n:
            k = (n + b) // d
            a, b, c, d = c, d, k * c - a, k * d - b
            if a>0:
                yield Rational(b, a)


def reciprocal_pair_iterator_r(r: Rational) -> Iterator[Tuple[Rational, Rational]]:
    """
    Find all solutions to 
        1/a + 1/b = r
    when r is a Rational number and a<=b.  The return is a generator 
    of pairs of Rational numbers (Rational(1,a), Rational(1,b)).
    USAGE:  `for a, b in reciprocal_pair_iterator_r(r):`
    """
    for a, b in reciprocal_pair_iterator(r.p, r.q):
        yield (Rational(1,a), Rational(1,b))

def reciprocal_pair_iterator(p: int, q: int) -> Iterator[Tuple[int, int]]:
    """
    Find all solutions to 
        1/a + 1/b = p/q
    with a<=b.
    USAGE:  `for a, b in reciprocal_pair_iterator(p, q):`
    """
    if p==0:
        return(False)
    for i in sorted(square_divisors(q)): # divisors of q**2 in order to avoid double factorization
        if i<=q:
            j = q**2//i
            if (i+q) % p == 0 and (j+q) % p ==0:
                a = (i+q)//p 
                b = (j+q)//p
                yield((a,b))

def reciprocal_pal_pair_iterator_r(r: Rational) -> Iterator[Tuple[Rational, Rational]]:
    """
    Find all solutions to 
        1/a + 1/b = r
    when r is a Rational number and a<=b and a and b are palindromes.  
    The return is a generator of pairs of Rational numbers (Rational(1,a), Rational(1,b)).
    USAGE:  `for a, b in reciprocal_pair_iterator_r(r):`
    """
    for a, b in reciprocal_pal_pair_iterator(r.p, r.q):
        yield (Rational(1,a), Rational(1,b))


def reciprocal_pal_pair_iterator(p: int, q: int) -> Iterator[Tuple[int, int]]:
    """
    Find all solutions to 
        1/a + 1/b = p/q
    with a<=b where a and b are palindromes.
    USAGE:  `for a, b in reciprocal_pal_pair_iterator(p, q):`
    """
    if p==0:
        return(False)
    for i in sorted(square_divisors(q)): # divisors of q**2 in order to avoid double factorization
        if i<=q:
            j = q**2//i
            if (i+q) % p == 0 and (j+q) % p ==0:
                a = (i+q)//p
                if is_palindromic(a):
                    b = (j+q)//p
                    if is_palindromic(b):
                        yield((a,b))


def egyptian_pair_iterator(p: int, q: int) -> Iterator[Tuple[int, int]]:
    """
    Find all solutions to 
        1/a + 1/b = p/q
    with a<b.
    USAGE:  `for a, b in egyptian_pair_iterator(p, q):`
    """
    for a, b in reciprocal_pair_iterator(p, q):
        if a<b:
            yield (a,b)


def egyptian_pair_iterator_r(r: Rational) -> Iterator[Tuple[Rational, Rational]]:
    """
    Find all solutions to 
        1/a + 1/b = r
    when r is a Rational number and a<=b.  The return is a generator 
    of pairs of Rational numbers (Rational(1,a), Rational(1,b)).
    USAGE:  `for a, b in egyptian_pair_iterator_r(r):`
    """
    for a, b in reciprocal_pair_iterator_r(r):
        if a.q<b.q:
            yield (a,b)
    
def egyptian_pal_pair_iterator(p: int, q: int) -> Iterator[Tuple[int, int]]:
    """
    Find all solutions to 
        1/a + 1/b = p/q
    with a<b and a and b are palindromes.
    USAGE:  `for a, b in egyptian_pal_pair_iterator(p, q):`
    """
    for a, b in reciprocal_pal_pair_iterator(p, q):
        if a<b:
            yield (a,b)


def egyptian_pal_pair_iterator_r(r: Rational) -> Iterator[Tuple[Rational, Rational]]:
    """
    Find all solutions to 
        1/a + 1/b = r
    when r is a Rational number and a<=b and a and b are palindromes.  
    The return is a generator of pairs of Rational numbers (Rational(1,a), Rational(1,b)).
    USAGE:  `for a, b in reciprocal_pair_iterator_r(r):`
    """
    for a, b in reciprocal_pal_pair_iterator_r(r):
        if a.q<b.q:
            yield (a,b)

def reciprocal_iterator_(p: int, 
                          q: int, 
                          k: int, 
                          pal_min=1, 
                          strict=False) -> Iterator[Tuple[int]]:
    """
    Iterate over all palindromic reciprocals of the rational r with exactly 
    k summands.  In other words find all solutions to 
        p/q = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 <= p_2 <= ... <= p_k,
    or p_1<p_2<...<p_k if strict=True.
    """
    if k==1:
        if p==1:
            return((q,))
    if k==2:
        if strict:
            for p1, p2 in egyptian_pair_iterator(p, q):
                yield (p1, p2)
        else:
            for p1, p2 in reciprocal_pair_iterator(p, q):
                yield (p1, p2)
    if k>=3:
        pal_min = max(pal_min, q // p)
        pal_max = ((k*q)//p)+1
        #print(f"pal_min={pal_min}, pal_max={pal_max}")
        for p1 in range(pal_min, pal_max):
            r1 = Rational(p,q)-Rational(1,p1)
            if r1>0:
                if k==3:
                    if strict:
                        for p2, p3 in egyptian_pair_iterator(r1.p, r1.q):
                            if p2>p1:
                                yield (p1, p2, p3)
                    else:
                        for p2, p3 in reciprocal_pair_iterator(r1.p, r1.q):
                            if p2>=p1:
                                yield (p1, p2, p3)
                else:
                    for sol in reciprocal_iterator_(r1.p, r1.q, k-1, 
                                                       pal_min=pal_min, strict=strict):
                        if strict:
                            if sol[0]>p1:
                                yield (p1,)+sol
                        else:
                            if sol[0]>=p1:
                                yield (p1,)+sol



def reciprocal_pal_iterator_(p: int, 
                          q: int, 
                          k: int, 
                          pal_min=1, 
                          strict=False) -> Iterator[Tuple[int]]:
    """
    Iterate over all palindromic reciprocals of the rational r with exactly 
    k summands.  In other words find all solutions to 
        p/q = 1/p_1 + 1/p_2 + ... + 1/p_k
    where p_1, p_2, ..., p_k are palindromes and
    and p_1 <= p_2 <= ... <= p_k if strict=False, 
    or p_1<p_2<...<p_k if strict=True.
    """
    if k==1:
        if p==1 and is_palindromic(q):
            return((q,))
    if k==2:
        if strict:
            for p1, p2 in egyptian_pal_pair_iterator(p, q):
                yield (p1, p2)
        else:
            for p1, p2 in reciprocal_pal_pair_iterator(p, q):
                yield (p1, p2)
    if k>=3:
        pal_min = max(pal_min, q // p)
        pal_max = ((k*q)//p)+1
        #print(f"pal_min={pal_min}, pal_max={pal_max}")
        for p1 in pal_iterator(pal_min, pal_max):
            r1 = Rational(p,q)-Rational(1,p1)
            if r1>0:
                if k==3:
                    if strict:
                        for p2, p3 in egyptian_pal_pair_iterator(r1.p, r1.q):
                            if p2>p1:
                                yield (p1, p2, p3)
                    else:
                        for p2, p3 in reciprocal_pal_pair_iterator(r1.p, r1.q):
                            if p2>=p1:
                                yield (p1, p2, p3)
                else:
                    for sol in reciprocal_pal_iterator_(r1.p, r1.q, k-1, 
                                                        pal_min=pal_min, 
                                                        strict=strict):
                        if strict:
                            if sol[0]>p1:
                                yield (p1,)+sol
                        else:
                            if sol[0]>=p1:
                                yield (p1,)+sol


def reciprocal_iterator(p: int, q: int, k: int) -> Iterator[Tuple[int]]:
    """
    Find all solutions to 
        p/q = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 <= p_2 <= ... <= p_k.
    """
    for sol in reciprocal_iterator_(p, q, k, pal_min=1, strict=False):
        yield sol

def reciprocal_iterator_r(r: Rational, k: int) -> Iterator[Tuple[Rational]]:
    """
    Find all solutions to 
        r = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 <= p_2 <= ... <= p_k with r a given Rational number.
    """
    for sol in reciprocal_iterator_(r.p, r.q, k, pal_min=1, strict=False):
        s =tuple([Rational(1, p) for p in sol])
        yield s

def egyptian_iterator(p: int, q: int, k: int) -> Iterator[Tuple[int]]:
    """
    Find all solutions to 
        p/q = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 < p_2 < ... < p_k.
    """
    for sol in reciprocal_iterator_(p, q, k, pal_min=1, strict=True):
        yield sol

def egyptian_iterator_r(r: Rational, k: int) -> Iterator[Tuple[Rational]]:
    """
    Find all solutions to 
        r = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 < p_2 < ... < p_k with r a given Rational number.
    """
    for sol in reciprocal_iterator_(r.p, r.q, k, pal_min=1, strict=True):
        s =tuple([Rational(1, p) for p in sol])
        yield s


def reciprocal_pal_iterator(p: int, q: int, k: int) -> Iterator[Tuple[int]]:
    """
    Find all solutions to 
        p/q = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 <= p_2 <= ... <= p_k with palindromic p_i.
    """
    for sol in reciprocal_pal_iterator_(p, q, k, pal_min=1, strict=False):
        yield sol


def reciprocal_pal_iterator_r(r: Rational, k: int) -> Iterator[Tuple[Rational]]:
    """
    Find all solutions to 
        r = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 <= p_2 <= ... <= p_k with palindromic p_i.
    """
    for sol in reciprocal_pal_iterator_(r.p, r.q, k, pal_min=1, strict=False):
        s =tuple([Rational(1, p) for p in sol])
        yield s


def egyptian_pal_iterator(p: int, q: int, k: int) -> Iterator[Tuple[int]]:
    """
    Find all solutions to 
        p/q = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 < p_2 < ... < p_k with palindromic p_i.
    """
    for sol in reciprocal_pal_iterator_(p, q, k, pal_min=1, strict=True):
        yield sol


def egyptian_pal_iterator_r(r: Rational, k: int) -> Iterator[Tuple[Rational]]:
    """
    Find all solutions to 
        r = 1/p_1 + 1/p_2 + ... + 1/p_k
    satisfying p_1 < p_2 < ... < p_k with palindromic p_i.
    """
    for sol in reciprocal_pal_iterator_(r.p, r.q, k, pal_min=1, strict=True):
        s =tuple([Rational(1, p) for p in sol])
        yield s


def pal_iterator_(n_digits: int, first: int=-1, last: int=-1) -> Iterator[int]:
    """
    Iterate over palindromic integers with n_digits between first and last.
    """
    is_odd = n_digits%2
    n_free = n_digits//2 + is_odd
    nn = n_digits-1
    values = []
    for i in range(n_digits//2):
        values.append(10**(nn-i)+10**i)
    if is_odd:
        values.append(10**(nn-(n_digits//2)))
    if first==-1 or first<10**nn:
        first = 10**nn
    if last==-1 or last>=10**(nn+1):
        last = 10**(nn+1)
    # For first = 23456 and last = 23993 we should iterate over digit strings
    #     (2,3,4), (2,3,4), ... , (2,3,9)
    # if first = 23456 and last = 24793 then the digit strings should be 
    #     (2,3,4), (2,3,4), ... , (2,3,9), (2,4,0), (2,4,1), ... (2,4,5)
    # i.e. all numbers from 234 up to and including 245
    if first == 10**nn and last == 10**(nn+1):
        its = [range(1,10)]
        for i in range(n_free-1):
            its.append(range(10))
        for dig_string in itertools.product(*its):
            yield sum([d*v for d,v in zip(dig_string, values)])
    else:
        first_digits = tuple([int(c) for c in str(first)])
        if last == 10**(nn+1):
            last_digits = tuple([int(c) for c in str(last-1)])
        else:
            last_digits = tuple([int(c) for c in str(last)])
        its = [range(first_digits[0], last_digits[0]+1),]
        for i in range(1,n_free):
            if len(its[-1])>1:
                its.append(range(10))
            else:
                its.append(range(first_digits[i], last_digits[i]+1))
        for dig_string in itertools.product(*its):
            if dig_string>=first_digits[:n_free] and dig_string<=last_digits[:n_free]:
                num = sum([d*v for d,v in zip(dig_string, values)])
                if num>=first and num<last:
                    yield num
                else:
                    if num>=last:
                        break                                        

def pal_iterator(first: int, last: int) -> Iterator[int]:
    """
    Iterate over palindromic integers in the range [first, last).
    USAGE:  `for n in pal_iterator(first, last):`
    """
    nd1 = len(str(first))
    nd2 = len(str(last))+1
    for dd in range(nd1, nd2):
        for n in pal_iterator_(dd, first, last):
            yield n


def lookup_table_(n: int, weight: List[int], l: int) -> List[Tuple[int]]:
    """
    Private helper function for pal_div_iterator_.  The idea is to 
    create a reverse lookup table that maps integer with the same or
    fewer digits than n to the remainder of the integer when divided by n. 
    """
    assert(len(weight)==l)
    table = []
    for i in range(n):
        table.append([])
    for tail in itertools.product(range(10), repeat=l):
        v = sum([w*d for (w,d) in zip(weight, tail)]) % n
        index = (n-v)%n
        table[index].append(tail)
    return(table)


def pal_div_iterator_(n_digits: int, n: int, first: int=-1, last: int=-1)-> Iterator[int]:
    """
    Iterate over all palindromic integers with n_digits between 
    first and last that are divisible by n.
    USAGE:  for pal in pal_div_iterator(n_digits, div, first, last):
    """
    # the code doesn't work correctly when n_digits==len(str(n)) or len(str(n))+1
    assert(n_digits>len(str(n))+2) 
    is_odd = n_digits%2
    n_free = n_digits//2 + is_odd
    nn = n_digits-1
    values = []
    reduced_values = []
    for i in range(n_digits//2):
        values.append(10**(nn-i)+10**i)
        reduced_values.append((10**(nn-i)+10**i)%n)
    if is_odd:
        values.append(10**(nn-(n_digits//2)))
        reduced_values.append(( 10**(nn-(n_digits//2)) )%n)
    if first==-1 or first<10**nn:
        first = 10**nn
    if last==-1 or last>=10**(nn+1):
        last = 10**(nn+1)

    lookup_length = len(str(n))
    table = lookup_table_(n, reduced_values[-lookup_length:], lookup_length)

    vv = values[:-lookup_length]
    vr = values[-lookup_length:]
    first_choice = range(1,10)
    if n%2==0:
        first_choice = [2,4,6,8]
    if n%5==0:
        first_choice = [5,]
    if first == 10**nn and last == 10**(nn+1):
        its = [first_choice,]
        for i in range(n_free-1-lookup_length):
            its.append(range(10))
        for dig_string in itertools.product(*its):
            s = sum([d*v for d,v in zip(dig_string, vv)])
            for t in table[s%n]:
                r = s+sum([d*v for d,v in zip(t, vr)])
                yield r
    else:
        first_digits = tuple([int(c) for c in str(first)])
        if last == 10**(nn+1):
            last_digits = tuple([int(c) for c in str(last-1)])
        else:
            last_digits = tuple([int(c) for c in str(last)])
        first_choice_reduced = [i for i in
                                range(first_digits[0], last_digits[0]+1) 
                                if i in first_choice]
        if len(first_choice_reduced)>0: # otherwise we can skip the whole thing
            its = [first_choice_reduced,]
            for i in range(1,n_free-lookup_length):
                if len(its[-1])>1:
                    its.append(range(10))
                else:
                    its.append(range(first_digits[i], last_digits[i]+1)) 
            for dig_string in itertools.product(*its):
                if (dig_string>=first_digits[:n_free-lookup_length] and 
                    dig_string<=last_digits[:n_free-lookup_length]):
                    s = sum([d*v for d,v in zip(dig_string, vv)])
                    for t in table[s%n]:
                        r = s+sum([d*v for d,v in zip(t, vr)])
                        if r>=first and r<last:
                            yield r
                        else:
                            if r>=last:
                                break




def pal_div_iterator(n: int, start: int, stop: int) -> Iterator[int]:
    """
    Efficiently iterate over palindromes that are multiples 
    of n in the range [start, stop).
    USAGE:  for pal in pal_div_iterator(n, first, last):
    """
    assert(stop>=start)
    if len(str(start))<len(str(n))+3:
        stop1 = 10**(len(str(n))+3)
        nd1 = len(str(stop1))
        nd2 = len(str(stop))+1
        if stop>=stop1:
            for i in pal_iterator(start, stop1):
                if i%n==0:
                    yield i
            for nd in range(nd1, nd2):
                for i in pal_div_iterator_(nd, n, stop1, stop):
                    yield i
        else:
            for i in pal_iterator(start, stop):
                if i%n==0:
                    yield i
    else:
        nd1 = len(str(start))
        nd2 = len(str(stop))+1
        for nd in range(nd1, nd2):
            for i in pal_div_iterator_(nd, n, start, stop):
                yield i


if __name__ == "__main__":
    pass
   