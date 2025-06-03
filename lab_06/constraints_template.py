"""
Lab 06 ▸ Exercise 1 — Generic Backtracking CSP Solver
=====================================================
Takeaways:
    • Recursive-Backtracking (RT Fig 6-5)  → DFS in assignment space.
    • **MRV** picks the variable with the fewest remaining values.
    • **LCV** orders values least-constraining-first.
    • Optional **Forward-Checking** & **AC-3** (switches for Challenge).
"""

from __future__ import annotations
from collections import deque, defaultdict
from copy import deepcopy
from typing import Dict, List, Callable, Tuple, Optional

Var      = str
Val      = str
Domain   = List[Val]
Assign   = Dict[Var, Val]
Neighbor = Dict[Var, List[Var]]

# --------------------------------------------------------------------------- #
#  Core CSP class                                                             #
# --------------------------------------------------------------------------- #
class CSP:
    def __init__(
        self,
        variables: List[Var],
        domains: Dict[Var, Domain],
        neighbors: Neighbor,
        constraint: Callable[[Var, Val, Var, Val], bool],
    ):
        self.V     = variables
        self.D     = deepcopy(domains)
        self.N     = neighbors
        self.cons  = constraint
        self.steps = 0  # nodes explored – for stats

    # ----- helpers --------------------------------------------------------- #
    def is_complete(self, A: Assign) -> bool:
        return len(A) == len(self.V)

    def is_consistent(self, var: Var, val: Val, A: Assign) -> bool:
        """Binary constraints only (map-colouring)."""
        return all(self.cons(var, val, nb, A[nb]) for nb in self.N[var] if nb in A)

    # ----- MRV / Degree heuristic ----------------------------------------- #
    def select_unassigned_var(self, A: Assign) -> Var:
        unassigned = [v for v in self.V if v not in A]
        # MRV
        m = min(unassigned, key=lambda v: len(self.D[v]))
        # Tie-break with *degree* (more neighbours ⇒ harder)
        min_size = len(self.D[m])
        densest  = [v for v in unassigned if len(self.D[v]) == min_size]
        return max(densest, key=lambda v: len(self.N[v]))

    # ----- LCV ------------------------------------------------------------- #
    def order_domain_vals(self, var: Var) -> Domain:
        def lcv_score(val):
            return sum(
                1
                for nb in self.N[var]
                for nb_val in self.D[nb]
                if not self.cons(var, val, nb, nb_val)
            )
        return sorted(self.D[var], key=lcv_score)

    # ---------------------------------------------------------------------- #
    #  Forward-Checking & AC-3 utilities                                      #
    # ---------------------------------------------------------------------- #
    def forward_check(self, var: Var, val: Val, removals: List[Tuple[Var, Val]]):
        """Prune inconsistent values from neighbours."""
        for nb in self.N[var]:
            if val in self.D[nb]:               # same colour -> illegal
                self.D[nb].remove(val)
                removals.append((nb, val))
                if not self.D[nb]:
                    return False
        return True

    def restore(self, removals: List[Tuple[Var, Val]]):
        for v, val in removals:
            self.D[v].append(val)

    def ac3(self) -> bool:
        """Revise every arc until arc-consistent."""
        queue = deque((Xi, Xj) for Xi in self.V for Xj in self.N[Xi])
        while queue:
            Xi, Xj = queue.popleft()
            if self.revise(Xi, Xj):
                if not self.D[Xi]:
                    return False
                for Xk in self.N[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    def revise(self, Xi: Var, Xj: Var) -> bool:
        revised = False
        for x in self.D[Xi][:]:
            if not any(self.cons(Xi, x, Xj, y) for y in self.D[Xj]):
                self.D[Xi].remove(x)
                revised = True
        return revised

    # ---------------------------------------------------------------------- #
    #  Backtracking Search                                                   #
    # ---------------------------------------------------------------------- #
    def backtracking_search(self, *, forward_check=False, use_ac3=False) -> Optional[Assign]:
        A: Assign = {}
        domains_backup = deepcopy(self.D)  # keep original for stats
        if use_ac3 and not self.ac3():     # Challenge: pre-process
            return None
        solution = self._backtrack(A, forward_check)
        self.D = domains_backup            # restore for possible re-runs
        return solution

    def _backtrack(self, A: Assign, fc: bool) -> Optional[Assign]:
        if self.is_complete(A):
            return A
        self.steps += 1
        var = self.select_unassigned_var(A)
        for val in self.order_domain_vals(var):
            if self.is_consistent(var, val, A):
                A[var] = val
                removals: List[Tuple[Var, Val]] = []
                domain_ok = True
                if fc:                        # Forward-Checking
                    domain_ok = self.forward_check(var, val, removals)
                if domain_ok:
                    res = self._backtrack(A, fc)
                    if res:
                        return res
                # undo
                if fc:
                    self.restore(removals)
                del A[var]
        return None

# --------------------------------------------------------------------------- #
#  Map-colouring instances                                                    #
# --------------------------------------------------------------------------- #
def adj_constraint(X: Var, x: Val, Y: Var, y: Val) -> bool:
    """X and Y may not share a colour if they are neighbours."""
    return x != y

def create_australia_csp() -> CSP:
    states = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
    colours = ["R", "G", "B"]
    domains = {s: colours[:] for s in states}
    neighbours = {
        "WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "SA": ["WA", "NT", "Q", "NSW", "V"],
        "Q": ["NT", "SA", "NSW"], "NSW": ["SA", "Q", "V"], "V": ["SA", "NSW"], "T": []
    }
    return CSP(states, domains, neighbours, adj_constraint)

# Self-test: solve Australia CSP when run directly -------------------------- #
if __name__ == "__main__":
    csp = create_australia_csp()
    sol = csp.backtracking_search(forward_check=False, use_ac3=False)
    print("Solution:", sol)
    print("Nodes expanded:", csp.steps)
