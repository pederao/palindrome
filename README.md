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

with $\left\\{a_i\right\\}_{i=1}^n$ being distinct palindromes and $a_1$, $a_2$ and $a_3$ possibly being the palindrome 0. This code-base supports exploration of these statements and the notebook `examples.ipynb` shows the various tools and how to use them.

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

## Solver module

To discover reciprocal palindromic representations of fractions we need to solve problems of the form

$$
\min_{\\mathbf{a}}\sum_i a_i
$$

subject to

$$
\sum_i a_i w_i = t
$$

and $a_i\in \\{0,1\\}$ for all $i$, where $\mathbf{w}$ and $t$ are a prescribed vector of positive integers and $t$ a target sum.
This type of problem belongs to the knapsack problem category which is known to be NP-complete.

Alternatively, we also allow for the constraint alternative $a_i\in\\{0,1,2,3,\ldots\\}$ which is a linear diophantine equation, also known as an integer programming problem. The solvers are respectively:

- `exact_knapsack`: A recursive solver for the exact knapsack problem.
- `egyptian_stack_search`: A stack based solver for the exact knapsack problem.
- `reciprocal_pal_stack_search`: A stack based solver for the corresponding linear integer programming problem.

There are also two solvers in the palindrome module; namely `egyptian_pal_pair_iterator` and `reciprocal_pal_pair_iterator` that can work wonders for fractions with small denominators and can also be used to prove that there is no shorter representation.

# Results so far

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

Possibly for these numbers the issue is that the density of palindromes that are a multiple of the denominators is very low. Also, we can compute the smallest integer such that $10^a-1$ is divisibly by the trouble prime $p$. This number is called the order of 10 modulo $p$. By Fermat's little theorem we know that the worst case is $a=p-1$ which happens for exactly 21 of the 78 numbers on our list:

```
379, 389, 419, 433, 461, 491, 571, 577, 593, 701,
743, 811, 821, 823, 857, 887, 937, 953, 971, 977,
983
```

In fact for a total of 59 of the trouble makers do we have that the order is greater than 100. The two smallest orders are 26 for 859 and 27 for 243. If we take a look at $10^26-1$ we can get a glimpse of why at least $10^{26}-1$ won't work as a base palindrome. The palindromic divisors of $10^{26}-1$ are:

```
9_449, 1_111_111_111_111, 3_333_333_333_333, 9_999_999_999_999, 10_000_000_000_001, 12_222_222_222_221, 30_000_000_000_003, 36_666_666_666_663, 90_000_000_000_009, 1_010_101_010_101_010_101_010_101, 3_030_303_030_303_030_303_030_303, 9_090_909_090_909_090_909_090_909, 11_111_111_111_111_111_111_111_111, 33_333_333_333_333_333_333_333_333, 99_999_999_999_999_999_999_999_999
```

Since there is a jump from 4 digits to 11 digits its understandable that the shortest representation of $\frac{1}{859}$ would be $\frac{11}{9449}$ using this base. Also, anomalous about 859 is that the first two palindromes that are multiples of 859 are
9,449 and 1,699,961, so there is a big jump there as well.

We expect a priori that the density of the palindromes dividing a given number $n$ should be roughly $1/n$ and the density for palindromes less than $10^{12}$ is essentially $0.99/n$ for all the cases except for 243, 486, 729, 972 which have densities of roughly $1/20n$ whereas 625 and 985 have densities about $1/2n$.

## General fractions

For fractions $\frac{p}{q}$ with $1\leq p, q\leq 100$ we have found representations satisfying the conjecture for all fractions. There are over 6000 such fractions with $\mathrm{gcd}(p,q)=1$, so this is pretty good computational evidence in support of the conjecture.

The longest representations where

$$
\begin{align}
\frac{35}{71} = &\frac{1}{6} + \frac{1}{8} + \frac{1}{9} + \frac{1}{22} + \frac{1}{66} + \frac{1}{77} + \frac{1}{141} + \frac{1}{292} + \frac{1}{494} + \frac{1}{858} + \frac{1}{1001} + \frac{1}{1881} + \frac{1}{2002} + \frac{1}{2112} + \frac{1}{6006} + \\
& \frac{1}{7007} + \frac{1}{66066} + \frac{1}{82928} + \frac{1}{84348} + \frac{1}{121121} + \frac{1}{141141} + \frac{1}{171171} + \frac{1}{297792} + \frac{1}{616616} + \\
& \frac{1}{880088} + \frac{1}{990099} + \frac{1}{27422472} +\frac{1}{63366336} + \frac{1}{1211441121} + \frac{1}{27449894472} + \frac{1}{232596695232}
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

It's worth noting that even for a small fraction like $8/5$ quite a few terms are needed:

$$
\frac{8}{5} = 1 + \frac{1}{2} + \frac{1}{11} + \frac{1}{121} + \frac{1}{2662} + \frac{1}{3993} + \frac{1}{5445} + \frac{1}{59895}.
$$

# Solution Method

To motivate the core idea behind the solution methodologies we are going to try to write $1/14$ as a sum of reciprocal palindromes. We will start without worrying about the palindromes being distinct. So first we find palindromes that are multiples of $14$ as follows:

```
>>> list(palindrome.pal_div_iterator(14,14,1000))
> [252, 434, 616, 686, 868]
```

Each of these palindromes will automatically give us a reciprocal representation like this:

$$
\frac{1}{14} = \frac{18}{252} = \frac{31}{434} = \frac{44}{616} = \frac{49}{686} = \frac{62}{868}
$$

So the smallest number of fractions needed here is 18. To improve on this we take a page out of the egyptian fraction playbook. If we subtract a fraction with a palindromic denominator close "enough" to $18/252$ the numerator will become smaller. For the closest reciprocal palindrome is $1/22$ since 22 is the next palindrome:

```
>>> palindrome.next_pal(14)
> 22
```

We have

$$
\frac{18}{252}-\frac{1}{22} = \frac{2}{77}
$$

which gives us the much shorter representation

$$
\frac{1}{14} = \frac{1}{22}+\frac{2}{77}.
$$

However, this procedure seems a bit ad hoc. How do we know that we get a palindrome in the numerator after we subtract off $1/22$? We can't in general expect such luck. The way to improve our luck is to find palindromes that somehow "fit together". For example if we list all the divisors of 252, 434, 616, 686, 868 we will find that some of the divisors are also palindromes. For 252 and 434 there are no palindrome divisors smaller than the number, but for 686 and 868 there are also the factors 343 and 434. This will help reduce the number of factors needed since we can write

$$
\frac{49}{686} = \frac{1}{686}+\frac{24}{343}
$$

and

$$
\frac{62}{868} = \frac{31}{434}.
$$

This didn't get us below 18, but take a look at the remaining number $616=2^3\cdot 7\cdot 11$. We have:

```
>>> list(palindrome.palindrome_divisors(616, 14))
> [22, 44, 77, 88, 616]
```

In other words 616 has the palindromic divisors 22, 44, 77, 88 and 616 itself. We now try to write $1/14$ in terms of these:

$$
\frac{1}{14} = \frac{a_1}{22}+\frac{a_2}{44}+\frac{a_3}{77}+\frac{a_4}{88}+\frac{a_5}{616}
$$

If we multiply by 616 we get a linear diophantine equation

$$
44 = 28 a_1 + 14 a_2 + 8 a_3 + 7 a_4 + a_5.
$$

To get a short representation we simply need to get $a_1+a_2+a_3+a_4+a_5$ to be as small as possible. For egyptian palindromic representations we additionally require that $a_i$ is either 0 or 1. In this example we cannot have a solution with only 2 terms since $28+14=42<44$. However, as we saw before we can solve it with 3 terms as such: $44= 28 + 2 \cdot 8$. Correspondingly this gives the solution $1/14=1/22+2/77$ that we saw before. We can also try to get an egyptian palindromic representation. Since 28+14=42$ we cannot have both $a_1=1$ and $a_2=1$ since this would force $a_5=2$. However, if we let $a_1=1$, $a_2=0$ we see that $a_3=a_4=a_5=1$ gives the egyptian palindromic representation:

$$
\frac{1}{14} = \frac{1}{22}+\frac{1}{77}+\frac{1}{88}+\frac{1}{616}.
$$

In general solving these integer diophantine equations while minimizing the sum of $a_i$ with the constraint $a_i\geq 0$, can be done using mixed integer linear programming or using diophantine linear equation solvers. I have refrained from using both of these and instead written a recursive greedy search algorithm that I called `stack_search`. The open source linear programming solvers I found did not work with arbitrary sized integers (big integers), which very quickly led to problems even for finding solutions to $1/n$ for $n<100$. It's quite possible that sympy's diophantine solvers could work - but it gives you the general solution and not necessarily the one for which the sum of $a_i$ is minimized. We have our own solver, but it might not be as efficient as some of the open source solvers.

When the constraint $a_i\in\{0,1\}$ is added, the problem becomes a knapsack problem with an equality constraint. Although, this is in general NP complete, it's easy to write a dynamic program to solve. We used a recursion approach that used bounding from above and below to avoid unnecessary recursion.

## Multiples of 10

We hit a snag however when we try to use this approach with a number that is a multiple of 10, since no palindrome can be a multiple of 10. To get around this we need to split up the number such that the factors of 2 and 5 are separated. Now, $1\10$ itself is a really tough one, so we will start by looking at what happens to $1/30$. We write $30=5\times 6$ and look for palindromes that are multiples of 5 and 6 and are also larger than 30. The first such palindromes are $55$ and $66$. Let's try solving

$$
\frac{1}{30} = \frac{a_1}{55}+\frac{a_2}{66}.
$$

Cross-multiplying by $330=\mathrm{lcm}(55,66)$ gives
$11 = 6a_1+5a_2$ with the obvious solution $a_1=a_2=1$ giving $\frac{1}{30}=\frac{1}{55}+\frac{1}{66}$.

Things are however, not always this straightforward, so let's consider a more complex example, so that the difficulties become more apparent. Consider $\frac{1}{60}$ with the factorization $60=2^2\cdot 3\cdot 5$ and let's look for palindromes that are multiples of $12=2^2\cdot 3$ and $15=3\cdot 5$ respectively with some shared factors. One such possibility is $252,252=2^2\cdot 3^2\cdot 7 \cdot 11\cdot 13$ and $585=3^2\cdot 5\cdot 13$. Next we calculate $\mathrm{lcm}(252252, 585) =1261260$ and we find all of its palindromic divisors larger than 60:

```
>>> list(palindrome.palindrome_divisors(1261260, 60))
> [66, 77, 99, 252, 585, 858, 1001, 2002, 2772, 3003, 4004, 5005, 6006, 7007, 9009, 252252]
```

This gives the equation

$$
\frac{1}{60} = \frac{a_1}{66}+\frac{a_2}{77}+\frac{a_3}{99}+\cdots + \frac{a_{15}}{9009}+\frac{a_{16}}{252252}.
$$

Cross multiplying by $1,261,260$ gives the diophantine equation

$$
\begin{align}
21021 =& 19110 a_1 + 16380 a_2 +12740a_3 + 5005a_4 + 2156a_5 + 1470a_6 + 1260a_7+\\
&630a_8+455a_9+420a_{10}+315a_{11}+252a_{12}+210a_{13}+180a_{14}+140a_{15}+5a_6
\end{align}
$$

It can then be checked that $a_2=a_5=a_6=a_9=a_{10}=a_{15}=1$ with all other coefficients 0 solves the problem since we then get
$16380+2156+1470+455+420+140=21021$ as required. This is a solution with 5 coefficients. We can actually use the `palindrome.egyptian_pal_iterator` with $k=5$ to verify that there are no solutions with only 5 terms. Thus this gives the shortest possible representation for $1/60$, i.e.

$$
\frac{1}{60} = \frac{1}{77}+\frac{1}{585}+\frac{1}{858}+\frac{1}{2772}+\frac{1}{3003}+\frac{1}{9009}.
$$

Just to double check that we can solve the knapsack problem, let's use our library function::

```
>>> import sympy, solver
>>> x = [66, 77, 99, 252, 585, 858, 1001, 2002, 2772, 3003, 4004, 5005, 6006, 7007, 9009, 252252]
>>> target = sympy.lcm(x)//60
>>> weight = [sympy.lcm(x) // i for i in x]
>>> score, a = solver.exact_knapsack(weight, capacity=target)
>>> score, a
> (6, [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
```

We can now get the denominators back like so:

```
>>> [x[i] for i in range(len(a)) if a[i] > 0]
> [77, 585, 858, 2772, 3003, 9009]
```

Glorious isn't it! Now the name of the game becomes how to make the choices to come up with the list for the palindromic denominators. Why did we for example choose 252,252 as the base palindrome for 12 and 585 as the base palindrome for 15? This was indeed done through some kind of brute force search, but maybe something smarter is possible?
