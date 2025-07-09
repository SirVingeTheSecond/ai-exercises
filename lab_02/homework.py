"""
Lecture 3 Lab ▸ Homework — Farmer, Wolf, Goat & Cabbage (BFS)
============================================================================
Exam tip: the puzzle often reappears with **different passengers or bank
labels**. Change only the CONFIG block below; no other edits needed.

CONFIG
------------
• BANKS......... side labels (default 'W'=west, 'E'=east)
• ENTITIES...... ordered list; first MUST be the boat driver (e.g. Farmer)
• INIT_STATE.... tuple of starting sides, len = len(ENTITIES)
• GOAL_STATE.... where you want everyone to end up
• UNSAFE_PAIRS.. list of tuples     (prey, predator)  – wrong alone together

The algorithm auto‑builds successor moves and validity checks from these
settings.
"""
from collections import deque
from typing import List, Tuple, Sequence

# ── CONFIG ─────────────────────────────────────────────────────────────────
BANKS: Tuple[str, str] = ("W", "E")
ENTITIES: Tuple[str, ...] = ("Farmer", "Wolf", "Goat", "Cabbage")
INIT_STATE: Tuple[str, ...] = ("W", "W", "W", "W")
GOAL_STATE: Tuple[str, ...] = ("E", "E", "E", "E")
UNSAFE_PAIRS: List[Tuple[int, int]] = [  # indexes into ENTITIES
    (1, 2),  # Wolf eats Goat
    (2, 3),  # Goat eats Cabbage
]

# ── DERIVED FUNCTIONS ──────────────────────────────────────────────────────
DRIVER_IDX: int = 0  # first entity must pilot the boat


def opposite(side: str) -> str:
    a, b = BANKS
    return b if side == a else a


def is_valid(state: Sequence[str]) -> bool:
    """Return False if any unsafe pair is alone without the driver."""
    driver_side = state[DRIVER_IDX]
    for predator, prey in UNSAFE_PAIRS:
        if state[predator] == state[prey] != driver_side:
            return False
    return True


def successor_fn(state: Tuple[str, ...]) -> List[Tuple[str, ...]]:
    """Generate all legal successor states (driver alone or driver + one)."""
    succ: List[Tuple[str, ...]] = []
    driver_side = state[DRIVER_IDX]
    # Move driver alone
    candidate = list(state)
    candidate[DRIVER_IDX] = opposite(driver_side)
    if is_valid(candidate):
        succ.append(tuple(candidate))
    # Move driver + each passenger on same side
    for idx, side in enumerate(state):
        if idx == DRIVER_IDX or side != driver_side:
            continue
        candidate2 = list(candidate)  # start from driver‑moved version
        candidate2[idx] = opposite(side)
        if is_valid(candidate2):
            succ.append(tuple(candidate2))
    return succ

# ── BFS ENGINE ─────────────────────────────────────────────────────────────
class Node:
    __slots__ = ("state", "parent")

    def __init__(self, state: Tuple[str, ...], parent: "Node | None" = None):
        self.state, self.parent = state, parent

    def path(self) -> List[Tuple[str, ...]]:
        out, n = [], self
        while n:
            out.append(n.state)
            n = n.parent
        return out[::-1]


def bfs() -> List[Tuple[str, ...]] | None:
    fringe: deque[Node] = deque([Node(INIT_STATE)])
    explored: set[Tuple[str, ...]] = set()
    while fringe:
        node = fringe.popleft()
        if node.state == GOAL_STATE:
            return node.path()
        if node.state in explored:
            continue
        explored.add(node.state)
        for s in successor_fn(node.state):
            if s not in explored:
                fringe.append(Node(s, node))
    return None


# ── DEMO RUN ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    sol = bfs()
    if sol:
        for step, st in enumerate(sol):
            print(f"{step:2}: {st}")
        print("\nMoves:", len(sol) - 1)
    else:
        print("No solution found.")
