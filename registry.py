"""
Module for storing shortest reciprocal palindromic representation of fractions.
Whenever a shorter fraction is added the previous one is removed and 
can no longer be retrieved.

DATABASES:
    'PalindromeRegistry': Stores shortest reciprocal representation of 1/n when 
                          repetitions are allowed.
    `EgyptianRegistry`: Stores shortest reciprocal representation of any fraction
                        where up to 3 palindromic integers are allowed.  This is
                        the database to track the conjecture.

HELPER FUNCTIONS:

"""
import os, time
import json, datetime
import sympy
from sympy import Rational
from sympy.ntheory import is_palindromic
from typing import List, Tuple, Dict, Any, Union, Iterator


class BaseRegistry():
    """
    Base class for storing shortest reciprocal palindromic representations.

    
    The registry uses a lock file so that multiple processes can read 
    and write at the same time.

    Please respect the efforts of others and don't falsely claim results 
    as your own.  If you don't want credits, simply omit the discoverer field.
    """
    def __init__(self, fname) -> None:
        self.fname = fname
        self.lock_fname = os.path.splitext(fname)[0]+'.lck'
        self.score = {} # number of unit palindromes needed
        self.registry = {}
        self.load()


    def load(self) -> None:
        """
        load the registry from a file, but check the lock file first
        to make sure that another process isn't writing to the file.
        """
        for i in range(5): # max tries to get lock is 5
            try:
                with open(self.lock_fname, 'x') as lockfile:
                    # write the PID of the current process so you can debug
                    # later if a lockfile can be deleted after a program crash
                    lockfile.write(f"pid={os.getpid()}")
                break
            except IOError:
                print(f"Another process is reading from {self.fname} waiting #{i}.")
                time.sleep(10)
        assert(i<5)
        if os.path.exists(self.fname):
            with open(self.fname, 'r') as f:
                reg_dict = json.load(f)
            for r in reg_dict:
                self.add(force=True, **reg_dict[r])
        os.remove(self.lock_fname)


    def save(self) -> None:
        self.load() # make sure nothing is lost
        # need to convert rationals into pairs of ints to save as json?
        for i in range(5): # max tries to get lock is 5
            try:
                with open(self.lock_fname, 'x') as lockfile:
                    # write the PID of the current process so you can debug
                    # later if a lockfile can be deleted after a program crash
                    lockfile.write(f"pid={os.getpid()}")
                break
            except IOError:
                print(f"Another process is reading from {self.fname} waiting #{i}.")
                time.sleep(10)
        with open(self.fname, 'w') as f:
            # need to convert rationals into strings to save as json.
            # sometimes r will be an integer and not a Rational, but this still
            # works.  Moreover note that the add method will convert to Rational
            # or int as needed, so this key is irrelevant, save for reading the file.
            json_registry = { str(r): self.registry[r] for r in self.registry }
            json.dump(json_registry, f)
        os.remove(self.lock_fname) # release the lock

    def credits(self, r: Any) -> str:
        if r in self.registry:
            if self.registry[r]['date']:
                credits_str = f"({self.registry[r]['discovered_by']}: {self.registry[r]['date']})"
            else:
                credits_str = f"({self.registry[r]['discovered_by']})"
        else:
            credits_str = ""
        return(credits_str)

    def score_str(self, r: Any) -> str:
        if r in self.score:
            return(f"[{self.score[r]}]")
        else:
            return("")
        

class EgyptianRegistry(BaseRegistry):
    """
    A register that keeps track of the most efficient representations of p/q
    as a sum of unique palindromes and reciprocal palindromes.  
    The maximum number of allowed palindromes is 3.

    $$
    \\frac{p}{q} = \\sum_{i=1}^k p_j + \\sum_{j=k+1}^n \\frac{1}{p_j}
    $$

    where k<=3 and p_j are all distinct palindromes.  Not that a representation 
    like $2+1/2$ is not allowed because of the repetition of 2. 
    """
    
    def __init__(self) -> None:
        fname = 'egyptian_palindromes.json'
        super().__init__(fname)
        self.score = {} # number of unit palindromes needed
        self.registry = {}
        self.load()
    
      
    def display(self, r:Rational, credits: bool=False, score: bool=False) -> str:
        if r in self.registry:
            pal_str = [f'{p}' for p in self.registry[r]['palindromes']]
            den_str = [f'1/{q}' for q in self.registry[r]['reciprocal_palindromes']]
            display_str = f'{r} = '+' + '.join(pal_str+den_str)
        else:
            display_str = f'{r} = ?'
        if score:
            display_str += " " + self.score_str(r)  
        if credits:
            display_str += " " + self.credits(r)
        return(display_str)

            
    def latex(self, r:Rational) -> str:
        if r in self.registry:
            pal_str = [f'{p}' for p in self.registry[r]['palindromes']]
            den_str = [f'\\frac{{1}}{{{q}}}' for q in self.registry[r]['reciprocal_palindromes']]
            return(f'\\frac{{{r.p}}}{{{r.q}}} = '+' + '.join(pal_str+den_str))
        else:
            return(f'{sympy.latex(r)} = \\mathord{{?}}')
        

    def jupyter_display(self, r:Rational, 
                        credits: bool=False, score: bool=False) -> None:
        from IPython.display import display, Math
        latex_str = self.latex(r)
        if score:
            latex_str += f"\\ \\mathbf{{{self.score_str(r)}}}"
        if credits:
            latex_str += f"\\ \\mathrm{{{self.credits(r)}}}"
        return display(Math(latex_str))
    
                
    def add(self, 
            palindromes: List[int], 
            reciprocal_palindromes: List[int], 
            discovered_by: str='NN', 
            date='', 
            method='unknown', 
            force=False ) -> None:
        reciprocal_palindromes = [int(x) for x in reciprocal_palindromes] # to avoid getting numpy types
        reciprocal_palindromes = sorted(list(set(reciprocal_palindromes)))
        palindromes = [int(x) for x in palindromes]
        palindromes = sorted(list(set(palindromes)))
        if 1 in reciprocal_palindromes:
            reciprocal_palindromes.remove(1)
            palindromes.append(1)
        if len(palindromes)>3:
            print("WARNING: Representations can at most have 3 palindromic numerators.")
            return
        for p in palindromes:
            if p in reciprocal_palindromes:
                print(f"WARNING: The palindrome {p} is already used as a denominator.")
                return
        dd = Rational(0,1)
        for q in reciprocal_palindromes:
            dd += Rational(1,q)
            if not is_palindromic(q):
                print(f"WARNING: 1/{q} is not a palindromic denominator.")
                return
        for p in palindromes:
            dd += Rational(p,1)
            if not is_palindromic(p):
                print(f"WARNING: The numerator {p} is not a palindrome.")
        sc = len(reciprocal_palindromes)+len(palindromes)
        if ((dd not in self.score) or 
            (sc<self.score[dd]) or 
            (force and self.score[dd]<=sc)):
            if date=='':
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.registry[dd] = {'palindromes': palindromes, 
                                 'reciprocal_palindromes': reciprocal_palindromes,
                                 'discovered_by': discovered_by,
                                 'date': date,
                                 'method': method}
            self.score[dd] = sc
                

class PalindromeRegistry(BaseRegistry):
    """
    A register that keeps track of the most efficient representations of 1/n
    as a sum of reciprocal palindromes when repetitions are allowed.  The registry
    is a dictionary of dictionaries where the key palindrome_fractions is a list
    of tuples of two integers (p,q) with q being a palindrome.  Thus we have for
    registry[n] that
        1/n = p_1/q_1 + p_2/q_2 + ... + p_k/q_k,
    where each q_i is a palindrome.
    """
    
    def __init__(self):
        fname = 'reciprocal_palindromes.json'
        super().__init__(fname)
        self.score = {} # number of unit reciprocal palindromes needed
        self.registry = {}
        self.load()
        
        
    def simplify(self, fractions: List[Tuple[int, int]])-> List[Tuple[int, int]]:
            rats = {}
            for p,q in fractions:
                if q in rats:
                    rats[q].append(p)
                else:
                    rats[q] = [p,]
            new_fractions = []
            for q in rats:
                p = sum(rats[q])
                r = Rational(p,q)
                if r.q != q and is_palindromic(r.q) and (r.q not in rats):
                    new_fractions.append((r.p, r.q))
                else:
                    new_fractions.append((p, q))
            return(new_fractions)
    
    def add(self, 
            palindrome_fractions: List[Tuple[int, int]], 
            discovered_by: str='NN', 
            date='', 
            method='unknown', 
            force=False ) -> None:
        fractions = [(int(x[0]), int(x[1])) for x in palindrome_fractions] # to avoid getting numpy types
        fractions = self.simplify(fractions)
        dd = Rational(0,1)
        sc = 0
        for p,q in fractions:
            dd += Rational(p,q)
            sc += p
            if not is_palindromic(q):
                print(f"WARNING: {p/q} has a denominator that is not a palindrome.")
                return
        if dd.p==1: # not tracking general fractions?
            if ((dd.q not in self.score) or 
                (sc<self.score[dd.q]) or
                (force and self.score[dd.q]==sc)):
                self.registry[dd.q] = { 
                    'palindrome_fractions': palindrome_fractions,
                    'discovered_by': discovered_by,
                    'date': date,
                    'method': method}
                self.score[dd.q] = sc
        else:
            print(f"WARNING: denominator not 1 in sum({fractions})")

                
    def display(self, n: int, credits: bool=False, score: bool=False) -> str:
        if n in self.registry:
            str_list = [f'{p}/{q}' for p,q in self.registry[n]['palindrome_fractions']]
            display_str = f'1/{n} = '+' + '.join(str_list)
        else:
            display_str = f'1/{n} = ?'
        if score:
            display_str += " " + self.score_str(n)  
        if credits:
            display_str += " " + self.credits(n)
        return(display_str)
    
            
    def latex(self, n: int) -> str:
        if n in self.registry:
            str_list = [f'\\frac{{{p}}}{{{q}}}' for p,q in self.registry[n]['palindrome_fractions']]
            return(f'\\frac{{1}}{{{n}}} = '+' + '.join(str_list))
        else:
            return(f'\\frac{{1}}{{{n}}} = \\mathord{{?}}')

    def jupyter_display(self, n:int, 
                        credits: bool=False, score: bool=False) -> None:
        from IPython.display import display, Math
        latex_str = self.latex(n)
        if score:
            latex_str += f"\\ \\mathbf{{{self.score_str(n)}}}"
        if credits:
            latex_str += f"\\ \\mathrm{{{self.credits(n)}}}"
        return display(Math(latex_str))
