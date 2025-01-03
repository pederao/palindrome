import palindrome

def exact_knapsack(weight, capacity, max_score=1_000_000, depth=0):
    """
    Solve the exact knapsack problem min sum_i x_i*v_i = capacity and sum_i v_i < max_score
    In our setting v_i=1 or 0.  weight = [x_1, x_2, ..., x_n] is a list of integers.
    
    We use the convention that if score==max_score on return there was no solution
    
    USAGE: score, x = exact_knapsack(weight, capacity, max_score=50)
    """
#    global counter
#    counter += 1
    if len(weight)==0:
        if capacity==0:
            return(0,[])
        else:
            return(max_score, [])
    best_score = max_score
    best_x = []
    # quickly check if we have enough weight to reach capacity
    max_cap = sum(weight)
    if max_cap<capacity:
        #print("Insufficient weights")
        return(max_score, [])
    if depth>=max_score:
        return(max_score, [])
    
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
        return(max_score, [])
    
    #print(f"start={start}, new cap={capacity}")
    if capacity == 0:
        return(score, x)
    #if capacity<0:
    #    print(f"start_cap = {start_cap}, weight={weight}, x={x}, surplus={surplus}, cap={capacity}")
        
    if start>=npal or capacity<0:
        #print("Failed after surplus pruning")
        return(max_score, [])
    
    # Next, no weight>capacity can be used
    while(start<npal and weight[start]>capacity):
        #print(f"start={start}, surplus={surplus}, x = {x}")
        x[start] = 0
        surplus -= weight[start]
        start += 1
    #print(f"cap={cap}, surplus={surplus}")
    if surplus<0:
        #print("Insufficient capacity after removal of over-weights")
        return(max_score, [])

    #print(x, weight)
    #print(start, score, capacity, surplus)
    # Next we have to prepare for recursive call
    end=len(weight)
    for i in range(start,end-1):
        if surplus>=0:
            #print(f"Recursive call, cap={capacity}, surplus={surplus}, i={i}, x={x}")
            #print(f"i={i}, x={x}, weight={weight}, capacity={capacity}")
            #print(f"new_weight={weight[start:i]+weight[i+1:]}, capacity={capacity-weight[i]}")
            score_i, x_i = exact_knapsack(weight[i+1:], capacity-weight[i], max_score=max_score, depth=depth+score+1)
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
        # print(f"best_score={best_score}, max_score={max_score}, best_x={best_x}")
        return(best_score, best_x)
    return(max_score,[])
