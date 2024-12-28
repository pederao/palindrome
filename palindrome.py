"""
Module for palindrome related functions and classes.

ITERATORS:

- `pal_iterator`: Iterate over palindromic integers in a range.
- `pal_div_iterator`: Iterate over palindromic integers in a range that is a multiple
                        of a given divisor.
- `reciprocal_frac_iter`: Iterate over representations of a fraction as a 
                          sum of reciprocal integers.

DATABASES:


SOLVERS:

HELPER FUNCTIONS:

- `is_palindromic`: Check if a number is palindromic.
- `pal_floor`: Find the largest palindromic number less than or equal to a number.
- `pal_ceil`: Find the smallest palindromic number greater than or equal to a number.
"""
import sys, os
import json
import sympy
from sympy import factorint, init_printing, symbols, Rational
from sympy.ntheory import is_palindromic
import itertools
from itertools import product
from collections import defaultdict
from typing import List, Tuple, Dict, Any, Union

def pal_floor(n: int) -> int:
    """
    Find the largest palindromic number <= n.
    USAGE:  pal = pal_floor(n)
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

def prev_pal(n):
    """
    Return the largest palindrome <n.
    """
    if is_palindromic(n):
        return(pal_floor(n-1))
    else:
        return(pal_floor(n))


def pal_ceil(n: int) -> int:
    """
    Find the smallest palindromic number >=n.
    USAGE:  pal = pal_ceil(n)
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

def next_pal(n):
    """
    Return the largest palindrome >n.
    """
    if is_palindromic(n):
        return(pal_ceil(n+1))
    else:
        return(pal_ceil(n))
    

def pal_iterator_(n_digits, first=None, last=None):
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
    if first is None or first<10**nn:
        first = 10**nn
    if last is None or last>=10**(nn+1):
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
        #print(first_digits, last_digits, its)
        #print(last_digits[:n_free])
        for dig_string in itertools.product(*its):
            if dig_string>=first_digits[:n_free] and dig_string<=last_digits[:n_free]:
                num = sum([d*v for d,v in zip(dig_string, values)])
                if num<last:
                    yield num
                else:
                    break                                        

def pal_iterator(first, last):
    """
    Iterate over palindromic integers in the range [first, last).
    USAGE:  for n in pal_iterator(first, last):
    """
    nd1 = len(str(first))
    nd2 = len(str(last))+1
    for dd in range(nd1, nd2):
        for n in pal_iterator_(dd, first, last):
            yield n

if __name__ == "__main__":
    pass
   