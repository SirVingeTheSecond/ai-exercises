"""
Lab 05 ▸ Utility — Generic Alpha-Beta Pruning
====================================================
Takeaways:
    • `alpha_beta_search()` decouples search from game logic; games pass in
      `successors`, `is_terminal`, and `utility` callbacks.
    • Optional `max_depth` + `eval_fn` supports depth-limited search (heuristics).
    • Returns `(best_action, value)` for the maximising player.  :contentReference[oaicite:4]{index=4}
"""

from typing import Any, Callable, Iterable, Tuple, Optional

State      = Any
Action     = Any
Successors = Callable[[State], Iterable[Tuple[Action, State]]]
Test       = Callable[[State], bool]
Utility    = Callable[[State], int]
Heuristic  = Optional[Callable[[State], int]]


def alpha_beta_search(
    state: State,
    successors: Successors,
    is_terminal: Test,
    utility: Utility,
    *,
    max_depth: int | None = None,
    eval_fn: Heuristic = None,
    maximizing_player: bool = True,
) -> Tuple[Action, int]:
    """Return optimal action & value for the *maximising* player."""

    def max_value(s: State, α: float, β: float, depth: int) -> float:
        if is_terminal(s):
            return utility(s)
        if max_depth is not None and depth >= max_depth:
            return (eval_fn or utility)(s)
        v = float("-inf")
        for _, child in successors(s):
            v = max(v, min_value(child, α, β, depth + 1))
            if v >= β:
                return v            # β-cut
            α = max(α, v)
        return v

    def min_value(s: State, α: float, β: float, depth: int) -> float:
        if is_terminal(s):
            return utility(s)
        if max_depth is not None and depth >= max_depth:
            return (eval_fn or utility)(s)
        v = float("inf")
        for _, child in successors(s):
            v = min(v, max_value(child, α, β, depth + 1))
            if v <= α:
                return v            # α-cut
            β = min(β, v)
        return v

    best_action: Action | None = None
    best_val    = float("-inf") if maximizing_player else float("inf")

    for a, child in successors(state):
        val = min_value(child, float("-inf"), float("inf"), 1) \
              if maximizing_player else \
              max_value(child, float("-inf"), float("inf"), 1)
        if maximizing_player and val > best_val or \
           not maximizing_player and val < best_val:
            best_val, best_action = val, a

    return best_action, best_val
