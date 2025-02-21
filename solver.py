"""
Module for finding shortest reciprocal palindromic representation of fractions.

The solvers all solve the same problem to find the shortest reciprocal palindrome representation, but 
the reciprocal_pal_stack_search allows repetition.  The essence of the optimization problem is to minimize
over a given weights [w_1, w_2, ..., w_n]

    min sum_i a_i 

    subject to 
        sum_i a_i * w_i = capacity 
        and a_i = 0 or 1 with no allowed repetition
        or a_i in {0,1,2,3,...} with allowed repetition

SOLVERS:
    `exact_knapsack`: A recursive solver for the exact knapsack problem.
    `egyptian_stack_search`: A stack based solver for the exact knapsack problem.
    `reciprocal_pal_stack_search`: A stack based solver for the corresponding linear integer programming problem.

PROBLEM ITERATORS:
    `palindrome_seed_iterator`: Iterates over palindromes dividing the denominator and uses heuristics to speed up the search.

HELPER FUNCTIONS:
    `weights_from_palindrome`: Given a large integer seed_value, a numerator p and a denominator q calculate the 
                               capacity and weights for the knapsack or linear integer programming problem.
    `weights_from_palindrome_r`: Same, but p/q is given as a Rational.

"""

import bisect
import math
from typing import List, Tuple, Dict, Any, Union, Iterator
import sympy
from sympy import Rational, factorint
from sympy.ntheory import is_palindromic
import palindrome

def exact_knapsack(weight: List[int], capacity: int, max_score: int=1_000_000, depth: int=0, verbose: bool=False) -> Tuple[int, List[int], int]:
    """
    A recursive solver that solves the exact knapsack problem.

    Solve the exact knapsack problem: 
        min sum_i a_i
    subject to 
        a_i = 0 or 1, and
        sum_i a_i * w_i = capacity, and
        sum_i a_i < max_score
    weight = [w_1, w_2, ..., w_n] is a list of integers, and the solution is
    given by the vector of active weights: active = [a_1, a_2, ..., a_n].  
    The score upon successful completion is set to sum_a a_i and otherwise to max_score.
    
    USAGE: score, active, error_code = exact_knapsack(weight, capacity, max_score=50)

    error_code=0: no error and a solution was found
    error_code=1: no solution was found.

    Note that the running time for a weight vector with 48 entries and a max_score>=48 
    was roughly 5 minutes on my computer.  Already for 50 entries the algorithm may run 
    for several days.   For weight vectors with more than 48 entries use the 
    egyptian_stack_search that has facilities for early termination of the search.

    """
#    global counter
#    counter += 1
    if len(weight)==0:
        if capacity==0:
            return(0,[], 0)
        else:
            return(max_score, [], 0)
    best_score = max_score
    best_x = []
    # quickly check if we have enough weight to reach capacity
    max_cap = sum(weight)
    if max_cap<capacity:
        #print("Insufficient weights")
        return(max_score, [], 1)
    if depth>=max_score:
        return(max_score, [], 1)
    
    start_cap = capacity
    npal = len(weight)
    x = [0 for w in weight]
    surplus = max_cap - capacity
    
    # any weight>surplus must be included
    start = 0
    score = 0
    while(start<npal and weight[start]>surplus):
        #print(f"start={start}, x={x}, weight={weight}, surplus={surplus}, capacity={capacity}")
        x[start] = 1
        capacity -= weight[start]
        start += 1
        score += 1
        
    # if number of forced choices brings us above max_score, then bail out
    if depth+score>=max_score: # >=max_score-1???????????????
        return(max_score, [], 1)
    
    #print(f"start={start}, new cap={capacity}")
    if capacity == 0:
        return(score, x, 0)
    #if capacity<0:
    #    print(f"start_cap = {start_cap}, weight={weight}, x={x}, surplus={surplus}, cap={capacity}")
        
    if start>=npal or capacity<0:
        #print("Failed after surplus pruning")
        return(max_score, [], 1)
    
    # Next, no weight>capacity can be used
    while(start<npal and weight[start]>capacity):
        #print(f"start={start}, surplus={surplus}, x = {x}")
        x[start] = 0
        surplus -= weight[start]
        start += 1
    #print(f"cap={cap}, surplus={surplus}")
    if surplus<0:
        #print("Insufficient capacity after removal of over-weights")
        return(max_score, [], 1)

    #print(x, weight)
    #print(start, score, capacity, surplus)
    # Next we have to prepare for recursive call
    end=len(weight)
    for i in range(start,end-1):
        if surplus>=0:
            #print(f"Recursive call, cap={capacity}, surplus={surplus}, i={i}, x={x}")
            #print(f"i={i}, x={x}, weight={weight}, capacity={capacity}")
            #print(f"new_weight={weight[start:i]+weight[i+1:]}, capacity={capacity-weight[i]}")
            score_i, x_i, error_code = exact_knapsack(weight[i+1:], capacity-weight[i], max_score=max_score, depth=depth+score+1)
            if len(x_i)>0 and 1+score+score_i < best_score:
                #print(f"score={score}, weight={weight}, cap={capacity}, depth={depth}")
                #print(f"x={x}, x_i={x_i}, i={i}, start={start}, end={end}, score_i={score_i}, best_score={best_score}")
                for j in range(i-start):
                    x[start+j]=0
                x[i] = 1
                for j in range(i+1,end):
                    x[j] = x_i[j-i-1]
                #print(x, weight, start_cap)
                assert(sum([weight[i]*x[i] for i in range(npal)])==start_cap) # or something is wrong
                best_score = 1+score+score_i
                #max_score = best_score -- not sure why this isn't working
                best_x = [i for i in x]
                #print(best_score, best_x, weight)
        surplus -= weight[i]
    if best_score<max_score:
        if verbose and depth==0:
            print(f"best_score={best_score}")
        return(best_score, best_x, 0)
    return(max_score, [], 1)


def end_capacity_(weights: List[int], max_score: int)-> List[int]:
    """
    Private helper function for egyptian_stack_search.  
    
    Calculates the sum of the next max_score weights from a given point onward.  If the 
    sum is less than the remaining capacity from a given point then no solution is possible 
    from that point onwards.

    USAGE: cum_sum = end_capacity_(weights, max_score)

    If max_score = 3 and weights=[w_1, w_2, w_3, ..., w_n] then cum_sum would be equal to:
    cum_sum = [w_1+w_2+w_3, w_2+w_3+w_4, ...., w_{n-2}+w_{n-1}+w_n, w_{n-1}+w_n, w_n]

    """
    cum_sum = [0 for i in weights]
    for i in range(len(weights)):
        for j in range(i, min(i+max_score, len(weights))):
            cum_sum[i] += weights[j] 
    return(cum_sum)


def egyptian_stack_search(weight: List[int], capacity: int, max_score: int=1_000, max_tries: int=100_000_000, verbose: bool=True) -> Tuple[int, List[int], int]:
    """
    A stack based solver that avoids recursion to solve the exact knapsack problem.
    The user can set an early termination criteria by specifying max_tries.  The 
    default setting should terminate after roughly 5 minutes.

    Solves the exact knapsack problem: 
        min sum_i a_i
    subject to 
        a_i = 0 or 1, and
        sum_i a_i * w_i = capacity, and
        sum_i a_i < max_score
    weight = [w_1, w_2, ..., w_n] is a list of integers, and the solution is
    given by the vector of active weights: active = [a_1, a_2, ..., a_n].  
    The score upon successful completion is set to sum_a a_i and otherwise to max_score.
    
    USAGE: score, active, error_code = egyptian_stack_search(capacity, weights, max_score=1_000, max_tries=100_000_000)

    error_code=0: no error and a best solution was found
    error_code=1: no solution was found and all possibilities exhausted.
    error_code=-1: no solution was found and algorithm terminated early due to #tries reaching max_tries.

    If error==0 we should have sum([active[i]*weights[i] for i in range(len(active))])==capacity.
    
    On my computer it takes roughly 1 minute to try 20_000_000 combinations of weights.  With 1 billion tries
    the time would roughly be 50 minutes.
    
    """
    assert(capacity>0)
    # need to switch signs to make bisection search work properly
    target = -capacity
    weights = [-w for w in weight] 
    n = len(weights)
    best_score = max_score
    best_active = [-1 for i in weights]

    num_backtracks = 0
    cum_sum = end_capacity_(weights, n-1)
    search_start = [0 for i in weights]
    search_current = [0 for i in weights]
    search_stop = [n for i in weights]
    active = [0 for i in weights]
    search_current[0] = -1
    sp = 0
    cur_target = target
    cur_score = 0
    
    # Some sanity checks before starting the stack search.
    if weights[-1]<cur_target:
        print(f"Check your calling parameters, capacity={-cur_target} is < weights[-1]={-weights[-1]}")
        return(best_score, best_active, 1)
    if weights[-1]==cur_target:  # This is an edge case that doesn't work in our code
        best_score = 1
        best_active = [0 for i in active]
        best_active[-1] = 1
        return(best_score, best_active, 0)

    ii = search_current[sp]
    if weights[ii+1]<cur_target:
        # Typically target would be much lower than the first weight.  This
        # would rarely happen, cut our code would not work if it happens and
        # we enter the while look with the first weight being smaller than the 
        # target.
        for jj in range(n):
            if weights[jj]>=cur_target:
                ii = jj-1
                break
        search_current[sp] = ii
        #print(f"Starting search at {ii}")

    prev_backtrack_message = 0
    while sp>=0 and num_backtracks<max_tries:
        if num_backtracks%10_000_000 == 0:
            if num_backtracks!=prev_backtrack_message and verbose:
                print(f"#tries={num_backtracks:_}, best_score={best_score}")
                prev_backtrack_message = num_backtracks
                # to avoid getting the same message repeatedly as we descend the stack.
        search_current[sp] += 1
        i = search_current[sp]
        cur_target -= weights[i]
        active[i] = 1
        cur_score += 1
        #print(f"search @{i} in range: {search_start[sp]}:{search_stop[sp]}")
        #print(f"cur_score={cur_score}, active={active}")
        #print(f"weights[i]={weights[i]}")
        #assert(cur_score == sum(active))
        #assert(cur_target == target - sum([active[k]*weights[k] for k in range(len(active))]))

        if sp==0 and i==(n-1):
            #print("Search is at an end")
            break # We have come to the end

        if i<search_stop[sp] and cur_score<best_score:
            #print(f"bisect on weights: cur_target={cur_target}, indices:{search_start[sp]}:{search_end[sp]}")
            # i+1 instead of search_start[sp]?
            new_start = bisect.bisect_left(weights, cur_target, i+1, n)
            #print(f"new_start={new_start}, weight={weights[new_start]}, cur_target={cur_target}")
            # note < means > since we have flipped the signs.
            # this shouldn't strictly speaking happen much.
            #print(new_start)
            if weights[new_start]<cur_target: # don't descend a level in the stack, simply keep sp and move current
                #print("Backtrack due to insufficient remaining weights.")
                active[i] = 0
                cur_score -= 1
                cur_target += weights[i]
                num_backtracks += 1
                sp-=1
                active[search_current[sp]] = 0
                cur_score -= 2
                cur_target += weights[i]
                cur_target += weights[search_current[sp]]
                continue

            #print(f"new_start={new_start}, {weights[new_start]}")
            search_start[sp+1] = new_start
            if weights[new_start] == cur_target:
                #print("Success backtrack!")
                # found a match after adding new_start
                active[new_start] = 1
                cur_score += 1
                #print(f"Hooray, match! new_start={new_start} cur_target={cur_target}, {weights[new_start]}")
                #print(f"score={cur_score}, sp={sp}, search[sp-1]:{search_start[sp-1]}, {search_current[sp-1]}, {search_end[sp-1]}")
                #print(active)
                score = sum(active)

                #assert(score==cur_score)
                if score<best_score:
                    best_score = score
                    best_active = active.copy()
                    # update cum_sum, to accelerate the search
                    # don't need to find other solutions with same score, so use best_score-1
                    cum_sum = end_capacity_(weights, best_score-1) 
                    if verbose:
                        print(f"Best score = {score}")
                    #active_dens = [dens[i] for i in range(len(active)) if active[i]==1]
                    #print(active_dens)
                active[new_start] = 0
                cur_score -= 1

                # backtrack from success
                num_backtracks += 1
                active[i] = 0
                sp -= 1
                active[search_current[sp]] = 0
                cur_score -= 2
                cur_target += weights[i]
                cur_target += weights[search_current[sp]]
                continue
            else:
    #             if search_start[sp+1]==n:
    #                 #print("Search_start[sp+1] at end")
    #                 search_end[sp+1]=n
    #                 assert(False)
    #             else:
                #print(f"bisect on cum_sum: cur_target={cur_target}, indices:{search_start[sp]}:{search_end[sp]}")
                new_stop = bisect.bisect_left(cum_sum, cur_target, i+1, n)
                #print(f"target={cur_target}, new_start={new_start}, new_stop={new_stop}")
                #print(f"weight_start={weights[new_start]}, cum_sum_stop={cum_sum[new_stop]}")
                search_stop[sp+1] = new_stop
                # This is a shortcut to save time
                if new_stop<=new_start: # don't descend a level in the stack, simply keep sp and move current
                    #print("Same level backtrack")
                    active[i] = 0
                    cur_score -= 1
                    cur_target += weights[i]
                    num_backtracks += 1
                else:
                    if cum_sum[new_stop] == cur_target:
                        # print("cum_sum == cur_target")
                        # found a match after adding new_start
                        for ii in range(new_stop,n):
                            active[ii] = 1
                            cur_score += 1
                        #print(f"Hooray, match! new_start={new_start} cur_target={cur_target}, {weights[new_start]}")
                        #print(f"score={cur_score}, sp={sp}, search[sp-1]:{search_start[sp-1]}, {search_current[sp-1]}, {search_end[sp-1]}")
                        #print(active)
                        score = sum(active)

                        #assert(score==cur_score)
                        if score<best_score:
                            best_score = score
                            best_active = active.copy()
                            # update cum_sum, to accelerate the search
                            # don't need to find other solutions with same score, so use best_score-1
                            cum_sum = end_capacity_(weights, best_score-1) 
                            if verbose:
                                print(f"Best score = {score}")
                            #active_dens = [dens[i] for i in range(len(active)) if active[i]==1]
                            #print(active_dens)

                        for ii in range(new_stop,n):
                            active[ii] = 0
                            cur_score -= 1

                        # backtrack from success
                        num_backtracks += 1
                        active[i] = 0
                        sp -= 1
                        active[search_current[sp]] = 0
                        cur_score -= 2
                        cur_target += weights[i]
                        cur_target += weights[search_current[sp]]
                        continue
                    else:
                        sp+= 1
                        search_current[sp] = new_start-1
                        #print(f"Descending sp+=1, @{search_current[sp]} in {search_start[sp]}:{search_stop[sp]}")
        else: # if i<search_stop
            #print("Backtrack due to i>=search_stop")
            #print(f"sp={sp}, i={i}, range={search_start[sp]}:{search_stop[sp]}")
            num_backtracks += 1
            active[i] = 0
            sp-=1
            active[search_current[sp]] = 0
            cur_score -= 2
            cur_target += weights[i]
            cur_target += weights[search_current[sp]]
            #print(f"Exiting backtrack with sp={sp}, new_range: i={search_current[sp]}, range={search_start[sp]}:{search_stop[sp]}")
    if num_backtracks>=max_tries:
        if verbose:
            print("Reached max_tries, aborting search.")
    error_code = 0
    if best_score>=max_score:
        error_code = 1
    if num_backtracks>=max_tries:
        error_code = -1
            
    return(best_score, best_active, error_code)


def reciprocal_pal_stack_search(weight: List[int], capacity: int, max_score: int=-1, max_tries: int=10_000_000, verbose: bool=True) -> Tuple[int, List[int], int]:
    """
    A stack based solver that avoids recursion to solve an integer linear programming 
    problem related to a reciprocal palindrome representation.

    The user can set an early termination criteria by specifying max_tries.  The 
    default setting should terminate after roughly 5 minutes.

    Solves the exact knapsack problem: 
        min sum_i a_i
    subject to 
        a_i>=0 and an integer [i.e. in the set {0,1,2,...}]
        sum_i a_i * w_i = capacity, and
        sum_i a_i < max_score
    weight = [w_1, w_2, ..., w_n] is a list of integers, and the solution is
    given by the vector of active weights: active = [a_1, a_2, ..., a_n].  
    The score upon successful completion is set to sum_i a_i and otherwise to max_score.
    Also sum_i a_i * w_i = capacity if successful.
    
    USAGE: score, active, error_code = reciprocal_pal_stack_search(capacity, weights, max_score=-1, max_tries=100_000_000)

    error_code=0: no error and a best solution was found
    error_code=1: no solution was found and all possibilities exhausted.
 
     """
    best_score = max_score
    if best_score==-1:
        best_score = capacity+1

    if len(weight)==1:
        if capacity % weight[0] == 0:
            return(capacity//weight[0], [capacity//weight[0]], 0)
        else:
            return(max_score, [], 1)

    best_use = []
    npal = len(weight)
    iterations = 0
    max_use = [ min(best_score, capacity//x) for x in weight]

    if weight[-1] != 1:
        print("WARNING: The stack search may get stuck or be extremely slow if weights[-1]!=1.")

    used = [0,]*npal
    run_up = [0,]*npal
    cum_score = [0,]*npal
    sp = 0
    used[sp] = max_use[sp]
    cum_score[sp] = max_use[sp]
    run_up[sp] = used[sp] * weight[sp]
    back_track = False
    while (sp>=0 and iterations<max_tries):
        if back_track:
            used[sp] = 0 
            cum_score[sp] = 0
            run_up[sp] = 0
            back_track = False
            sp -= 1
            if sp<0:
                #print("Quitting")
                break
            if used[sp]<=0:
                back_track = True
                continue
            iterations += 1
            u = used[sp]-1
            used[sp] = u
            score = cum_score[sp-1] + u
            cum_score[sp] = score
            run_up[sp] = run_up[sp-1] + u * weight[sp]
        else:
            sp += 1
            if (sp>=npal):
                back_track = True
                sp = npal-1
                if weight[-1]>1:
                    for k in range(sp, 0, -1):
                        if weight[sp-1]%weight[-1] == 0:
                            # backtracking to this level will be useless,
                            # so we will manually backtrack extra levels.
                            used[sp] = 0 
                            cum_score[sp] = 0
                            run_up[sp] = 0
                            sp -= 1
                        else:
                            break
                    continue
                else:
                    print(weight)
                    print(max_use)
                    print(used)
                    print(run_up)
                    print(cum_score)
                    print(sp)
                    assert(False)
                    
            ds = weight[sp]
            u = int((capacity-run_up[sp-1])//ds)
            used[sp] = u
            score = cum_score[sp-1] + u
            cum_score[sp] = score
            if score>=best_score:
                back_track = True
                continue
            run_up[sp] = run_up[sp-1] + u * ds
            if run_up[sp] == capacity:
                back_track = True
                if score<best_score:
                    if verbose:
                        print(f"Hit : {used}, score={score}, its={iterations}")
                    best_score = score
                    best_use = used.copy()
    if len(best_use)>0:
        return(best_score, best_use, 0)
    else:
        return(best_score,[], 1) # no hits


def least_conflicting_palindrome_tuple_(N: int, conflict_list)-> Tuple[int, ...]:
    palindrome_sum = []
    if is_palindromic(N):
        palindrome_sum.append(N)
    if palindrome.has_palindromic_bipartition(N):
        for x in palindrome.pal_bipartition_iterator(N):
            if len(set(x)) == len(x): # repetitions are not allowed
                palindrome_sum.append(x)
    else:
        for x in palindrome.pal_tripartition_iterator(N):
            if len(set(x)) == len(x): # repetitions are not allowed
                palindrome_sum.append(x)
    least_conflicts = 4
    best_candidate = palindrome_sum[0]
    for palindromes in palindrome_sum:
        num_conflicts = 0
        for x in palindromes:
            if x in conflict_list:
                num_conflicts += 1
        if num_conflicts<least_conflicts:
            best_candidate = palindromes
            least_conflicts = num_conflicts
    return(best_candidate)


class ProblemWrapper:
    def __init__(self, capacity: int, weight: List[int], div_list: List[int], palindrome_tuple: Tuple[int, ...], seed_value: int = -1):
        self.capacity = capacity
        self.weight = weight
        self.div_list = div_list
        self.palindrome_tuple = palindrome_tuple
        self.seed_value = seed_value

def weights_from_number_r(seed_value: int, r: Rational)-> ProblemWrapper:
    """
    Given a number/seed value generate a set of palindrome denominators to use for the search.  The weight
    vector and the target can be used with the knapsack and stack_search optimization routines, and
    the div_list contains the palindromes needed to reconstruct the reciprocal palindromic representation.
    """
    return weights_from_number(seed_value, int(r.p), int(r.q))


def weights_from_number(seed_value: int, p: int, q: int)-> ProblemWrapper:
    """
    Given a number/seed value generate a set of palindrome denominators to use for the search for a representation
    for the rational p/q.  The weight vector and the target can be used with the knapsack and stack_search 
    optimization routines, and the div_list contains the palindromes needed to reconstruct the reciprocal 
    palindromic representation.

    USAGE: capacity, weight, div_list, palindrome_tuple = weights_from_number(seed_value, p, q)
    """
    min_value = q // p
    div_list = list(palindrome.palindrome_divisors(seed_value, min_value))
    capacity = (seed_value*p) // q
    palindrome_tuple = tuple()
    if p>q:
        N = p // q # integer portion of fraction
        # First off avoid fractions 1/1 that can just be written as 1.
        # By convention we put 1 in the palindrome portion of the solver
        if 1 in div_list:
            div_list.remove(1)
        palindrome_tuple = least_conflicting_palindrome_tuple_(N, div_list)
        for x in palindrome_tuple:
            if x in div_list:
                div_list.remove(x)
        weight = [seed_value*p for p in palindrome_tuple[::-1]]+[ seed_value // x for x in div_list ]
    else:
        weight = [ seed_value // x for x in div_list ]
    return(ProblemWrapper(capacity, weight, div_list, palindrome_tuple[::-1], seed_value))


def palindrome_seed_iterator_r(r: Rational, start_search: int=-1, end_search: int=10**12, 
                               min_num_divisors: int=4, max_num_divisors=48, 
                               step_size: int=-1, num_pals2: int=-1,
                                num_pals5: int=-1, verbose: bool=True, report_frequency: int=1000) -> Iterator[ProblemWrapper]:
    for i in palindrome_seed_iterator(int(r.p), int(r.q), start_search, end_search,
                                       min_num_divisors, max_num_divisors, step_size,
                                       num_pals2, num_pals5, verbose, report_frequency):
        yield i


def palindrome_seed_iterator(p: int, q:int, start_search: int, end_search: int, 
                             min_num_divisors: int=4, max_num_divisors: int=48, 
                             step_size: int=-1, num_pals2: int=-1,
                             num_pals5: int=-1, verbose: bool=True, report_frequency: int=1000) -> Iterator[ProblemWrapper]:
    """
    This function implements a fast version of the loop
        for seed_value in palindrome.pal_div_iterator(step_size, start_search, end_search)
            # some logic
            yield problem_wrapper
    However, there are complications when q is divisible by 10.
    """
    counter = 0 # for reporting progress
    if step_size == -1:
        step_size = q
    assert(step_size%q == 0)
    if start_search == -1:
        start_search = q
    if q%10 != 0:
        for seed_value in palindrome.pal_div_iterator(step_size, start_search, end_search):
            pw = weights_from_number(seed_value, p, q)
            if len(pw.div_list)<min_num_divisors or len(pw.div_list)>max_num_divisors:
                continue
            if sum(pw.weight)<pw.capacity:
                continue
            counter += 1
            if counter % report_frequency == 0:
                if verbose:
                    print(f"Tried {counter:_} seed values, currently at {int(seed_value):_}")
            yield pw
    else:
        factors = factorint(step_size)
        p2 = 2**factors[2]
        p5 = 5**factors[5]

        estimated_num_pals = int(math.sqrt(end_search-start_search)/q)
        if num_pals2==-1:
            num_pals2 = p5*int(math.sqrt(estimated_num_pals//(p2+p5)))
        if num_pals5==-1:
            num_pals5 = p2*int(math.sqrt(estimated_num_pals//(p2+p5)))
        if verbose:
            print(f"Using num_pals2={num_pals2}, num_pals5={num_pals5}.")
        
        step2 = step_size//p5
        pal2_list = []
        for k2 in palindrome.pal_div_iterator(step2, start_search, end_search):
            div_list2 = list(palindrome.palindrome_divisors(k2, q))
            if len(div_list2)>min_num_divisors and len(div_list2)<max_num_divisors:
                pal2_list.append(k2)
                if len(pal2_list)>=num_pals2:
                    break
        
        step5 = step_size//p2
        pal5_list = []
        for k5 in palindrome.pal_div_iterator(step5, start_search, end_search):
            div_list5 = list(palindrome.palindrome_divisors(k5, q))
            if len(div_list5)>min_num_divisors and len(div_list5)<max_num_divisors:
                pal5_list.append(k5)
                if len(pal5_list)>=num_pals5:
                    break
        if verbose:
            print(f"pal2_list: start={pal2_list[0]}, end={pal2_list[-1]}")
            print(f"pal5_list: start={pal5_list[0]}, end={pal5_list[-1]}")

        for k2 in pal2_list:
            for k5 in pal5_list:
                seed_value = sympy.lcm(k2, k5)
                pw = weights_from_number(seed_value, p, q)
                if len(pw.div_list)<min_num_divisors or len(pw.div_list)>max_num_divisors:
                    continue
                if sum(pw.weight)<pw.capacity:
                    continue
                counter += 1
                if counter % report_frequency == 0:
                    if verbose:
                        print(f"Tried {counter:_} seed values, currently at {int(seed_value):_}")
                        print(f"k2={k2:_}, k5={k5:_}")
                yield pw


    