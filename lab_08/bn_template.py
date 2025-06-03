"""
Lab 08 ▸ Exercise — Sprinkler Bayesian Network
=============================================
Results:
    P(WetGrass=true) ≈ 0.6471
    P(Sprinkler=true | WetGrass=true) ≈ 0.4298
"""

from __future__ import annotations
import itertools
from typing import Dict, List, Tuple

# ── Variable --------------------------------------------------------------- #
class Variable:
    def __init__(
        self,
        name: str,
        values: Tuple[str, str],
        cpt: Dict[Tuple[str, ...], Tuple[float, float]],
        parents: List["Variable"] | None = None,
    ):
        self.name = name
        self.idx  = {v: i for i, v in enumerate(values)}
        self.cpt  = cpt
        self.parents = parents or []

    def p(self, value: str, parent_vals: Tuple[str, ...]) -> float:
        return self.cpt[parent_vals][self.idx[value]]

# ── Bayesian Network ------------------------------------------------------- #
class BayesianNetwork:
    def __init__(self, nodes: List[Variable]):
        self.nodes = nodes
        self.index = {v.name: v for v in nodes}          # bug fixed

    # chain-rule joint
    def joint(self, world: Dict[str, str]) -> float:
        prob = 1.0
        for v in self.nodes:
            parents = tuple(world[p.name] for p in v.parents)
            prob *= v.p(world[v.name], parents)
        return prob

    # full enumeration marginals (handles dependent parents)
    def marginals(self) -> Dict[str, Dict[str, float]]:
        marg = {v.name: {"true": 0.0, "false": 0.0} for v in self.nodes}
        names = [v.name for v in self.nodes]
        for assignment in itertools.product(("true", "false"), repeat=len(self.nodes)):
            world = dict(zip(names, assignment))
            pj = self.joint(world)
            for n, val in world.items():
                marg[n][val] += pj
        return marg

    # enumeration query P(var=value | evidence)
    def query(self, var: str, value: str, evidence: Dict[str, str]) -> float:
        hidden = [n for n in self.nodes if n.name not in evidence and n.name != var]

        def total(val_choice: str) -> float:
            ev = evidence.copy(); ev[var] = val_choice
            tot = 0.0
            for combo in itertools.product(("true", "false"), repeat=len(hidden)):
                w = ev.copy()
                for h, vval in zip(hidden, combo):
                    w[h.name] = vval
                tot += self.joint(w)
            return tot

        num   = total(value)
        denom = total("true") + total("false")
        return num / denom

# ── CPTs from PDF ---------------------------------------------------------- #
P_C = {(): (0.5, 0.5)}
P_S = {("false",): (0.5, 0.5), ("true",): (0.1, 0.9)}
P_R = {("false",): (0.2, 0.8), ("true",): (0.8, 0.2)}
P_W = {
    ("false", "false"): (0.0, 1.0),
    ("true",  "false"): (0.9, 0.1),
    ("false", "true"):  (0.9, 0.1),
    ("true",  "true"):  (0.99, 0.01),
}

Cloudy   = Variable("Cloudy",   ("true", "false"), P_C)
Sprink   = Variable("Sprinkler",("true", "false"), P_S, [Cloudy])
Rain     = Variable("Rain",     ("true", "false"), P_R, [Cloudy])
WetGrass = Variable("WetGrass", ("true", "false"), P_W, [Sprink, Rain])

bn = BayesianNetwork([Cloudy, Sprink, Rain, WetGrass])

# ── Demo ------------------------------------------------------------------- #
if __name__ == "__main__":
    m = bn.marginals()
    print("Marginal probabilities:")
    for v in bn.nodes:
        print(f"  P({v.name}=true) = {m[v.name]['true']:.6f}")

    w = {"Cloudy":"false","Sprinkler":"true","Rain":"false","WetGrass":"true"}
    print("\nJoint(C=F,S=T,R=F,W=T) =", bn.joint(w))

    post = bn.query("Sprinkler", "true", {"WetGrass":"true"})
    print("P(Sprinkler=true | WetGrass=true) =", round(post, 4))
