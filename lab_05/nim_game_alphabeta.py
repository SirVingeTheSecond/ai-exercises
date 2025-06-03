"""
Lab 05 ▸ Exercise 3 — Alpha-Beta Pruning for Nim (engine-based)
==============================================================
"""

from nim_game_minimax import (           # helpers already exported  :contentReference[oaicite:5]{index=5}
    nim_is_terminal,
    nim_successors,
    nim_utility,
    START_STONES, MAX_REMOVE,
)
from alpha_beta import alpha_beta_search

# ---------------------------------------------------------------------------

def best_action(heap: int) -> int:
    """Optimal stones to remove for MAX."""
    action, _ = alpha_beta_search(
        heap,
        successors=nim_successors,
        is_terminal=nim_is_terminal,
        utility=nim_utility
    )
    return action

# ---------------------------------------------------------------------------
#  Play loop (human = MIN) ---------------------------------------------------
# ---------------------------------------------------------------------------
def play(heap: int = START_STONES, k: int = MAX_REMOVE):
    max_turn = True
    while not nim_is_terminal(heap):
        print(f"\nStones left: {heap}")
        if max_turn:
            take = best_action(heap)
            print(f"MAX removes {take}.")
        else:
            while True:
                try:
                    take = int(input(f"Your move 1-{min(k, heap)}: "))
                    if 1 <= take <= min(k, heap):
                        break
                except ValueError:
                    pass
            print(f"MIN removes {take}.")
        heap -= take
        max_turn = not max_turn
    print("\nMAX wins!" if not max_turn else "\nYou win!")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    play()
