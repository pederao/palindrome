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

with $\left\{a_i\right\}_{i=1}^n$ being distinct palindromes. This code-base supports exploration of these statements.
