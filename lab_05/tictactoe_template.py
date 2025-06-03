"""
Lab 05 ▸ Exercise 1 — Minimax Tic‑Tac‑Toe
========================================
Takeaways:
    • *Game state* encoded as length‑9 list; integers ⇒ empty squares, "X" / "O" ⇒ occupied.
    • Functions required by **minimax**: `is_terminal`, `utility_of`, `successors_of`.
    • Minimax explores **full game tree** (≤9! states); DFS via recursion (see slides, p. 6‑7).  fileciteturn14file6
    • WIN combos pre‑listed for O(1) winner test -> typical exam trick.

NOTE: you are MIN ("O"), computer is MAX ("X").
"""

from typing import List, Tuple

# --- helper: winning triples (row, col, diag) ------------------------------ #
WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),        # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),        # cols
    (0, 4, 8), (2, 4, 6)                    # diags
]

# ---------------------------------------------------------------------------
# 1. TERMINAL TEST
# ---------------------------------------------------------------------------

def is_terminal(state: List[int]) -> bool:
    """Return True if someone wins *or* board is full (draw)."""
    return winner(state) is not None or all(isinstance(v, str) for v in state)

# ---------------------------------------------------------------------------
# 2. UTILITY FUNCTION
# ---------------------------------------------------------------------------

def utility_of(state: List[int]) -> int:
    """+1 if X wins (MAX), −1 if O wins (MIN), else 0."""
    w = winner(state)
    if w == "X":
        return 1
    if w == "O":
        return -1
    return 0  # draw or non‑terminal (shouldn't be queried for non‑terminal but safe)

# ---------------------------------------------------------------------------
# 3. SUCCESSOR GENERATOR
# ---------------------------------------------------------------------------

def successors_of(state: List[int]) -> List[Tuple[int, List[int]]]:
    """Return list of (move, new_state) pairs for current player."""
    # Determine player: X starts; if counts equal ⇒ X to move else O.
    nX = sum(1 for v in state if v == "X")
    nO = sum(1 for v in state if v == "O")
    player = "X" if nX == nO else "O"

    succ = []
    for idx, v in enumerate(state):
        if isinstance(v, int):               # empty square labelled by int index
            new_state = state.copy()
            new_state[idx] = player
            succ.append((idx, new_state))
    return succ

# ---------------------------------------------------------------------------
#  Supporting helpers & existing minimax driver (unchanged) ------------------
# ---------------------------------------------------------------------------

def winner(state: List[int]):
    for i, j, k in WIN_LINES:
        if state[i] == state[j] == state[k] and state[i] in ["X", "O"]:
            return state[i]
    return None


def argmax(iterable, fn):
    return max(iterable, key=fn)


def minmax_decision(state: List[int]):
    """Return best move index for MAX using full minimax DFS."""
    infinity = float("inf")

    def max_value(st):
        if is_terminal(st):
            return utility_of(st)
        v = -infinity
        for (m, s) in successors_of(st):
            v = max(v, min_value(s))
        return v

    def min_value(st):
        if is_terminal(st):
            return utility_of(st)
        v = infinity
        for (m, s) in successors_of(st):
            v = min(v, max_value(s))
        return v

    move, _ = argmax(successors_of(state), lambda ms: min_value(ms[1]))
    return move

# ---------------------------------------------------------------------------
#  Pretty printing & main game loop ------------------------------------------
# ---------------------------------------------------------------------------

def display(state: List[int]):
    print("-----")
    for r in [0, 3, 6]:
        print(state[r], state[r+1], state[r+2])


def main():
    board: List[int] = list(range(9))  # initial 0..8 labels
    while not is_terminal(board):
        # Computer (MAX) move
        board[minmax_decision(board)] = "X"
        if is_terminal(board):
            break
        display(board)
        # Human (MIN) move
        valid = False
        while not valid:
            try:
                move = int(input("Your move (0‑8)? "))
                if board[move] == move:
                    board[move] = "O"
                    valid = True
                else:
                    print("Square occupied; try again.")
            except (ValueError, IndexError):
                print("Invalid input; use 0‑8.")
    display(board)
    result = utility_of(board)
    if result == 1:
        print("X (computer) wins!")
    elif result == -1:
        print("O (you) win!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
