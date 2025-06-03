"""
Lab 03 ▸ Homework — A* Vacuum Cleaner (4‑square world)
=====================================================
Takeaways:
    • **A*** search ⇒ f(n)=g+h finds *optimal* (shortest‑move) plan when h is admissible.
    • State = (location, A,B,C,D status) ⇒ |S| = 4×2⁴ = 64  (tractable graph).
    • Heuristic = count_dirty_squares → never over‑estimates ⇒ admissible & consistent.
    • Outputs: *path*, *total cost* (moves), *nodes expanded* — classic exam metrics.
"""

import heapq
from typing import List, Tuple

# ── generic A* scaffolding ─────────────────────────────────────────────────── #
class Node:
    """Lightweight search tree node (keeps only what BFS/A* needs)"""

    __slots__ = ("state", "path", "g")

    def __init__(self, state: Tuple, path: List[str], g: int):
        self.state, self.path, self.g = state, path, g  # g ≡ path‑cost so far

    # Priority queue compares on f(n)=g+h; we compute on‑the‑fly for speed
    def __lt__(self, other: "Node"):
        return False  # tie‑break handled by heap tuple (f,this)


def a_star_search(start_state: Tuple,
                  goal_test,
                  successors,
                  heuristic) -> Tuple[List[str], int, int]:
    """Generic A* that returns (action_path, cost, expanded_nodes)."""
    root = Node(start_state, [], 0)
    frontier: List[Tuple[int, Node]] = []
    heapq.heappush(frontier, (heuristic(start_state), root))
    explored = set()
    expanded = 0

    while frontier:
        f, current = heapq.heappop(frontier)
        if current.state in explored:
            continue  # cheaper path already processed
        explored.add(current.state)
        expanded += 1

        if goal_test(current.state):
            return current.path, current.g, expanded

        for action, new_state, step_cost in successors(current.state):
            if new_state in explored:
                continue
            g_new = current.g + step_cost
            child = Node(new_state, current.path + [action], g_new)
            heapq.heappush(frontier, (g_new + heuristic(new_state), child))

    return [], float("inf"), expanded  # failure (should not occur here)

# ── Vacuum‑world domain (4 squares linear: A‑B‑C‑D) ───────────────────────── #
POSITIONS = ["A", "B", "C", "D"]


def vac_initial_state() -> Tuple:
    """Start at A, all squares dirty."""
    return ("A", "Dirty", "Dirty", "Dirty", "Dirty")


def vac_goal_test(state: Tuple) -> bool:
    return all(s == "Clean" for s in state[1:])


def vac_successors(state: Tuple) -> List[Tuple[str, Tuple, int]]:
    """Generate (action, new_state, cost) where cost=1 per move."""
    loc, *statuses = state
    idx = POSITIONS.index(loc)
    succ = []

    # Suck
    if statuses[idx] == "Dirty":
        new_statuses = list(statuses)
        new_statuses[idx] = "Clean"
        succ.append(("Suck", (loc, *new_statuses), 1))

    # Move Right
    if idx < 3:
        succ.append(("Right", (POSITIONS[idx + 1], *statuses), 1))

    # Move Left
    if idx > 0:
        succ.append(("Left", (POSITIONS[idx - 1], *statuses), 1))

    return succ


def vac_heuristic(state: Tuple) -> int:
    """#Dirty squares ≤ moves needed ⇒ admissible."""
    return sum(1 for s in state[1:] if s == "Dirty")


# ── quick demo ─────────────────────────────────────────────────────────────── #
if __name__ == "__main__":
    path, cost, expanded = a_star_search(
        start_state=vac_initial_state(),
        goal_test=vac_goal_test,
        successors=vac_successors,
        heuristic=vac_heuristic,
    )

    print("Solution path :", " -> ".join(path))
    print("Total cost    :", cost)
    print("Nodes expanded:", expanded)
