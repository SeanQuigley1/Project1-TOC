"""
SAT Solver - DIMACS-like Multi-instance Format
----------------------------------------------------------
Project 1: Tough Problems & The Wonderful World of NP

INPUT FORMAT (multi-instance file):
-----------------------------------
Each instance starts with a comment and a problem definition:

c <instance_id> <k> <status?>
p cnf <n_vertices> <n_edges>
u,v
x,y
...

Example:
c 1 3 ?
p cnf 4 5
1,2
1,3
2,3
2,4
3,4
c 2 2 ?
p cnf 3 3
1,2
2,3
1,3

OUTPUT:
-------
A CSV file named 'resultsfile.csv' with columns:
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution


EXAMPLE OUTPUT
------------
instance_id,n_vars,n_clauses,method,satisfiable,time_seconds,solution
3,4,10,U,0.00024808302987366915,BruteForce,{}
4,4,10,S,0.00013304100139066577,BruteForce,"{1: True, 2: False, 3: False, 4: False}"
"""

from typing import List, Tuple, Dict
from src.helpers.sat_solver_helper import SatSolverAbstractClass
import itertools


class SatSolver(SatSolverAbstractClass):

    """
        NOTE: The output of the CSV file should be same as EXAMPLE OUTPUT above otherwise you will loose marks
        For this you dont need to save anything just make sure to return exact related output.
        
        For ease look at the Abstract Solver class and basically we are having the run method which does the saving
        of the CSV file just focus on the logic
    """


    def verifier(self, clauses:List[List[int]], assignments) -> int:
        # if all clauses true - success (True) - 1
        # else if some clauses true, others undeterminable, none false - perhaps (None) - -1
        # else if any clause is false - failure (False) - 0
        
        status = 1
        for clause in clauses:
            any_unknowns = False
            truthiness = False

            # need to see if any var (negated or not) will make the clause true, if 
            for var in clause:
                # inverted with (-) sign
                var_val = assignments[abs(var)]
                if var_val is None: 
                    any_unknowns = True
                    continue

                # negate variable value if needed
                if var < 0: var_val = not var_val

                # one true var = true clause, break
                if var_val: 
                    truthiness = True
                    break

            # if false clause entirely - we can return that these assignments don't work
            if not any_unknowns and not truthiness: 
                status = 0
                break

            # indeterminable - will continue searching clauses to ensure none are False
            if not truthiness and any_unknowns: status = -1

        return status
        

    def sat_backtracking(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        # mapping of boolean/assignments set to None (all untried at beginning)
        assignments = { k: None for k in range(1, n_vars + 1) }
        print(clauses)
        # will be used to quickly identify new var to try
        not_assigned = { k for k in range(1, n_vars + 1) }

        # initial empty stack - will be used to track tried components / backtracking functionality
        stack = []

        # initialize first var to get algorithm underway
        initial_var = not_assigned.pop()
        stack.append(initial_var)
        # start with True, shallow backtrack will flip from True -> False -> deep backtrack
        assignments[initial_var] = True


        # setting up first variable to test out
        # can make while loop condition True = because either works or not works will be determined - no risk of infinite loop
        while True:
            result = self.verifier(clauses, assignments)
            # works
            if result == 1:
                # set unseen vars to anything
                while not_assigned:
                    temp_var = not_assigned.pop()
                    assignments[temp_var] = True
                return (True, assignments)
            # assignment failed
            elif result == 0:
                # backtracking
                while stack:
                    top = stack[-1]

                    # was true -> now false
                    if assignments[top] == True: 
                        assignments[top] = False  
                        break

                    # was false, exhausted var - backtrack
                    else: 
                        assignments[top] = None
                        not_assigned.add(top)
                        stack.pop()
                # Unsatisfiable
                if not stack: return (False, {}) 
            # add additional assignment - inconclusive
            else:
                new_var = not_assigned.pop()
                assignments[new_var] = True
                stack.append(new_var)

    def sat_bruteforce(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        for test in product([True, False], repeat=n_vars): #make all combos
            
            assignments = { k+1: test[k] for k in range(n_vars) }
            
            if self.verifier(clauses, assignments) == 1:
                return (True, assignments) #found a match
        # couldnt find a match
        return (False, {})
    

    def sat_bestcase(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass

    def sat_simple(self, n_vars:int, clauses:List[List[int]]) -> Tuple[bool, Dict[int, bool]]:
        pass