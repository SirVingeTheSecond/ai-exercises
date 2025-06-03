"""
Lab 05 ▸ Exercise 2 — Minimax for Nim (single-heap variant)
==========================================================
Takeaways:
    • *Game state* = single integer `n` ⇒ #stones remaining (0 = terminal).
    • Legal actions: remove 1…k stones (here k = 3) — illustrates branching factor.
    • **Minimax** explores complete game tree; utility = +1 if MAX wins, −1 if MIN wins.

Run: you (MIN) play against perfect MAX.
"""

from functools import lru_cache

# ---------------------------------------------------------------------------
#  Parameters
# ---------------------------------------------------------------------------
MAX_REMOVE   = 3    # max stones removable per turn
START_STONES = 15

# ---------------------------------------------------------------------------
# 1. TERMINAL TEST
# ---------------------------------------------------------------------------
def is_terminal(n: int) -> bool:
    """True iff no stones remain."""
    return n == 0

# ---------------------------------------------------------------------------
# 2. UTILITY FUNCTION
# ---------------------------------------------------------------------------
def utility_of(n: int, player_max: bool = True) -> int:
    """
    Return +1 if MAX wins, −1 if MIN wins.
    Only called on *terminal* positions (n == 0).
    """
    # If it is MAX’s turn and the pile is empty, MAX has *lost* (−1).
    return -1 if player_max else 1

# ---------------------------------------------------------------------------
# 3. SUCCESSOR GENERATOR
# ---------------------------------------------------------------------------
def successors_of(n: int) -> list[int]:
    """List of legal next #stones after removing 1…k."""
    return [n - r for r in range(1, min(MAX_REMOVE, n) + 1)]

# ---------------------------------------------------------------------------
#  Minimax with memoisation ---------------------------------------------------
@lru_cache(maxsize=None)
def max_value(n: int) -> int:
    if is_terminal(n):
        return utility_of(n, player_max=True)
    v = -float("inf")
    for child in successors_of(n):
        v = max(v, min_value(child))
    return v

@lru_cache(maxsize=None)
def min_value(n: int) -> int:
    if is_terminal(n):
        return utility_of(n, player_max=False)
    v = float("inf")
    for child in successors_of(n):
        v = min(v, max_value(child))
    return v

def best_move(n: int) -> int:
    """Return stones to remove (1…k) that maximises MAX utility."""
    moves = {r: min_value(n - r) for r in range(1, min(MAX_REMOVE, n) + 1)}
    # Choose largest utility, tie-break with smallest r (faster win)
    return max(moves, key=lambda r: moves[r])

# ---------------------------------------------------------------------------
#  Interactive game (human = MIN) -------------------------------------------
# ---------------------------------------------------------------------------
def human_move(n: int) -> int:
    while True:
        try:
            r = int(input(f"You remove 1-{min(MAX_REMOVE, n)} stones: "))
            if 1 <= r <= min(MAX_REMOVE, n):
                return r
        except ValueError:
            pass
        print("Invalid move.")

def main():
    n = START_STONES
    player_max_turn = True   # MAX starts
    while not is_terminal(n):
        print(f"\nStones left: {n}")
        if player_max_turn:
            r = best_move(n)
            print(f"MAX removes {r} stone(s).")
        else:
            r = human_move(n)
        n -= r
        player_max_turn = not player_max_turn

    if player_max_turn:   # loop flipped after last move
        print("\nYou (MIN) win!")
    else:
        print("\nMAX wins!")

# ---------------------------------------------------------------------------
#  For nim_game_alphabeta.py
# ---------------------------------------------------------------------------
nim_is_terminal = is_terminal

def nim_successors(n: int) -> list[tuple[int, int]]:
    """
    Return list of (removed, new_heap) pairs for alpha-beta to iterate.
    """
    return [(r, n - r) for r in range(1, min(MAX_REMOVE, n) + 1)]

def nim_utility(n: int) -> int:
    """
    Utility for a *terminal* node from MAX’s perspective.
    """
    return utility_of(n, player_max=True)

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
