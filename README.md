# Palindromic Pandemonium

This project explores representations of fractions as sums of (unit) reciprocal palindromes such as

$$
\frac{1}{10} = \frac{1}{22} + \frac{1}{55}+\frac{1}{55}+\frac{1}{55}
$$

We have proven in a companion paper that all fractions can indeed be written as a sum of reciprocal palindromes and that this becomes impossible if we require the palindromes to be unique (i.e. egyptian fractions). This is because the sum of all reciprocal palindromes add up to approximately 3.370 and thus any fraction larger than that such as $\frac{7}{2}$ cannot be represented as a palindromic egyptian fraction.

Furthermore it has been conjectured that every fraction can be written in the form

$$
a_1+a_2+a_3+\sum_{i=4}^n \frac{1}{a_i}
$$

with $\left\\{a_i\right\\}_{i=1}^n$ being distinct palindromes. This code-base supports exploration of these statements.

## Palindrome module

The palindrome module contains iterators to return all palindromes in a given
range and all palindromes that are a multiple of a number n in a given range.
The module also contains iterators that give all solutions to
$$\frac{p}{q} = \frac{1}{p_1}+\frac{1}{p_2}+...+\frac{1}{p_k}$$
with $k$ a given number. If $p_1<p_2<\cdots<p_k$ we call the solution egyptian. Functions with \_r in the name takes Rational numbers as inputs, other functions takes integer input. Functions with \_pal only returns solutions where all numbers are palindromes.

For example to find all egyptian palindromic representations of 1 with 5 terms:

```
for sol in palindrome.egyptian_pal_iterator_r(Rational(1,1),5):
    print(sol)
```
