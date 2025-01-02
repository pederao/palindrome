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

`examples.ipynb` shows examples of most of the functions in palindrome.py.

## Registry module

This module contains two classes two store results and to record the discovery date and author for each of the reciprocal palindromic representations. The two classes are respectively: `PalindromeRegistry` and `EgyptianRegistry`. The `PalindromeRegistry` class allows repetitions of palindromes, so representations of $\frac{p}{q}$ can be obtained by repeating every palindrome occuring in the representation for $\frac{1}{q}$, therefore we only store representations of $\frac{1}{q}$ in the database. For the `EgyptianRegistry` class repetitions are not allowed and this database stores representations of any fraction. All fractions will be put in reduced form, so that $\mathrm{gcd}(p,q)=1$ before being a new entry to the database.

Each of the classes provides the methods `load`, `save`, `add`, `display`, `latex` and `jupyter_display`. If you add a new entry with your own discovery it will only be added to the database if the representation is shorter than what is already in the dictionary and the json file. Thus you will not be accidentally overwriting other peoples credits unless your discovery is indeed a shorter representation.

We have stored representations for each of the methods for unit fractions $\frac{1}{n}$ with $1\leq n\leq 1000$ and general fractions $\frac{p}{q}$ with $1\leq p,q\leq 100$.

## Results so far

We have succeeded in making reciprocal palindromic representations for all unit fractions for denominators less than 1000. For egyptian palindromic representations we have succeeded for all unif fractions with denominators less than $3^5=243$ and for all denominators less than 1000 with the exception of 78 cases. These are as follows:

```243, 347, 379, 389, 401, 419, 421, 433, 449, 461, 466, 486, 491, 547, 571,
577, 587, 593, 607, 613, 617, 622, 625, 631, 634, 641, 643, 653, 661, 662,
673, 674, 677, 691, 698, 701, 719, 723, 729, 733, 734, 743, 751, 753, 758,
761, 766, 769, 773, 778, 794, 809, 811, 821, 823, 827, 839, 841, 842, 853,
857, 859, 862, 866, 877, 887, 907, 911, 922, 937, 953, 971, 972, 977, 982,
983, 985, 997
```

Fundamentally, I don't believe that these are impossible to find representations for, but I also don't have a way to prove that. The best method we have for finding egyptian palindromic representations with a lot of terms is the exact knapsack algorithm that is in general NP-complete, so we get an exponential explosion in the computational cost. It is my hope that a fast, approximate version of the knapsack algorithm can knock off most of these 78 cases, and I hope someone will submit such a method. My knapsack implementation is also very inefficient in that it is done using recursion.

The 78 cases can be grouped into a few different groups. Firstly, it should be noted that 81 does not divide any palindromes smaller than $999,999,999=10^9-1$, and therefore any product of 81 will be difficult. We succeeded for 81, 162, 324, 405, 567, 648, 810 and 829, but not for 243, 486, 729 and 972 which are exactly the products of $3^5$ for which the smallest palindrome it divides is $29,799,999,792$ and $39,789,998,793$ in the case of $3^6=729$.

Powers of 5 are also difficult, and $5^4=625$ is on our list. The first dividing palindrome is $5,213,125$, but perhaps more importantly the shortest representation we found with repetitions allowed had 61 terms, which is much larger than our knapsack solver can handle. 985 had a representation with 93 terms and can be put in the same category. The complete list of denominators requiring more than 50 terms with repetitions allowed were: 243, 461, 486, 577, 625, 634, 673, 729, 823, 877, 887, 907, 972, 983, 985. The longest representation is 157 for 729.

Another category are large primes. I do not know exactly why these primes are trouble makers, but these primes we do not have egyptian palindromic representations for:

```
347, 379, 389, 401, 419, 421, 433, 449. 461, 491, 547, 571, 577, 587, 593,
607, 613, 617, 631, 641, 643, 653, 661, 673, 677, 691, 701, 719, 729, 733,
743, 751, 761, 769, 773, 809, 811, 821, 823, 827, 839, 853, 857, 859, 877,
887, 907, 911, 937, 953, 971, 977, 983, 997
```

For some of these primes, twice the prime is also on the list of missing representations:

```
379, 758
389, 778
421, 842
433, 866
461, 922
491, 982
```

For some of the missing numbers the shortest reciprocal palindromic representations has the form $\frac{k}{p}$ with $p$ being a palindrome. For example

$$
\begin{aligned}
\frac{1}{379} &= \frac{22}{8338}\\
\frac{1}{389} &= \frac{22}{8558}\\
\frac{1}{419} &= \frac{2}{838}\\
\frac{1}{449} &= \frac{2}{898}\\
\frac{1}{461} &= \frac{62}{28582}\\
\frac{1}{673} &= \frac{92}{61916}\\
\frac{1}{677} &= \frac{11}{7447}\\
\frac{1}{758} &= \frac{11}{8338}\\
\frac{1}{778} &= \frac{11}{8558}\\
\frac{1}{839} &= \frac{11}{9229}\\
\frac{1}{841} &= \frac{43}{36163}\\
\frac{1}{859} &= \frac{11}{9449}\\
\frac{1}{922} &= \frac{31}{28582}\\
\frac{1}{997} &= \frac{39}{38883}\\
\end{aligned}
$$

Possibly for these numbers the issue is that the density of palindromes that are a multiple of the denominators is very low. Also, we can compute the smallest integer such that $10^a-1$ is divisibly by the trouble prime $p$. The worst case is $a=p-1$ which happens for these primes

```
379, 389, 419, 433, 461, 491, 571, 577, 593, 701,
743, 811, 821, 823, 857, 887, 937, 953, 971, 977,
983
```

We expect a priori that the density of the palindromes dividing a given number $n$ should be roughly $1/n$ and the density for palindromes less than $10^{12}$ is essentially $0.99/n$ for all the cases except for 243, 486, 729, 972 which have densities of roughly $1/20n$ whereas 625 and 985 have densities about $1/2n$.

### General fractions

For fractions $\frac{p}{q}$ with $1\leq p, q\leq 100$ we have found representations satisfying the conjecture for all fractions. There are over 6000 such fractions with $\mathrm{gcd}(p,q)=1$, so this is pretty good computational evidence in support of the conjecture.

The longest representations where

$$
\begin{align}
\frac{35}{71} = &\frac{1}{6} + \frac{1}{8} + \frac{1}{9} + \frac{1}{22} + \frac{1}{66} + \frac{1}{77} + \frac{1}{141} + \frac{1}{292} + \frac{1}{494} + \frac{1}{858} + \frac{1}{1001} + \frac{1}{1881} + \frac{1}{2002} + \frac{1}{2112} + \\
& \frac{1}{6006} + \frac{1}{7007} + \frac{1}{66066} + \frac{1}{82928} + \frac{1}{84348} + \frac{1}{121121} + \frac{1}{141141} + \frac{1}{171171} + \frac{1}{297792} + \\
& \frac{1}{616616} + \frac{1}{880088} + \frac{1}{990099} + \frac{1}{27422472} +\frac{1}{63366336} + \frac{1}{1211441121} + \frac{1}{27449894472} + \frac{1}{232596695232}
\end{align}
$$

and

$$
\begin{align}
\frac{62}{71} = & \frac{1}{3} + \frac{1}{4} + \frac{1}{7} + \frac{1}{11} + \frac{1}{77} + \frac{1}{88} + \frac{1}{99} + \frac{1}{111} + \frac{1}{292} + \frac{1}{313} + \frac{1}{363} + \frac{1}{777} +\frac{1}{1221} + \frac{1}{3003} + \frac{1}{3443} + \\
& \frac{1}{7227} + \frac{1}{10001} + \frac{1}{11011} + \frac{1}{20002} + \frac{1}{29592} + \frac{1}{30003} + \frac{1}{33033} + \frac{1}{34743} + \frac{1}{37873} + \frac{1}{60006} + \frac{1}{84348} + \\
& \frac{1}{90009} + \frac{1}{330033} + \frac{1}{1539351} + \frac{1}{3161613} + \frac{1}{189939981}
\end{align}
$$
