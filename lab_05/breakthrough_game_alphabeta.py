"""
Lab 05 ▸ Exercise 4 — Alpha-Beta for *Breakthrough* (5x5)
=======================================================================
Takeaways:
    • Depth-limited α-β via shared engine; heuristic gives quick eval.
"""

from __future__ import annotations
import math, random
from typing import List, Tuple
from alpha_beta import alpha_beta_search                     # generic engine  :contentReference[oaicite:6]{index=6}

# --- board constants --------------------------------------------------------
N = 5
W, B, E = "W", "B", "."
DIR = {W: -1, B: 1}

Board  = List[List[str]]
Move   = Tuple[int, int, int, int]          # (r,c,r2,c2)
MAX_P  = W
MIN_P  = B

def start_board() -> Board:
    bd = [[E]*N for _ in range(N)]
    for c in range(N):
        bd[1][c] = B
        bd[N-2][c] = W
    return bd

# --- game-rule callbacks ----------------------------------------------------
def succ(bd: Board) -> List[Tuple[Move, Board]]:
    out = []
    for r in range(N):
        for c in range(N):
            p = bd[r][c]
            if p not in (W, B): continue
            dr = DIR[p]
            for dc in (0, -1, 1):
                r2, c2 = r+dr, c+dc
                if 0 <= r2 < N and 0 <= c2 < N:
                    target = bd[r2][c2]
                    fwd = dc == 0 and target == E
                    cap = dc != 0 and target == (B if p == W else W)
                    if fwd or cap:
                        nb = [row[:] for row in bd]
                        nb[r][c], nb[r2][c2] = E, p
                        out.append(((r, c, r2, c2), nb))
    return out

def terminal(bd: Board) -> bool:
    return any(x == W for x in bd[0]) or any(x == B for x in bd[-1]) \
        or all(x != W for row in bd for x in row) \
        or all(x != B for row in bd for x in row)

def utility(bd: Board) -> int:
    if any(x == W for x in bd[0]):  return +math.inf
    if any(x == B for x in bd[-1]): return -math.inf
    return 0

def heuristic(bd: Board) -> int:
    w = sum(x == W for row in bd for x in row)
    b = sum(x == B for row in bd for x in row)
    adv_w = max((N-1-r) for r in range(N) for c in range(N) if bd[r][c]==W) if w else 0
    adv_b = max(r for r in range(N) for c in range(N) if bd[r][c]==B) if b else 0
    return 10*(w-b) + (adv_w - adv_b)

# --- driver -----------------------------------------------------------------
DEPTH = 4

def best_move(bd: Board) -> Move:
    mv, _ = alpha_beta_search(
        bd,
        successors=succ,
        is_terminal=terminal,
        utility=utility,
        max_depth=DEPTH,
        eval_fn=heuristic,
        maximizing_player=True          # White is MAX
    )
    return mv

def render(bd: Board):
    symbols = {W:"▲", B:"▼", E:"."}
    print("\n  " + " ".join(map(str, range(N))))
    for i,row in enumerate(bd):
        print(i, " ".join(symbols[x] for x in row))

def play():
    bd = start_board()
    turn_max = True
    while not terminal(bd):
        render(bd)
        if turn_max:
            mv = best_move(bd)
            r,c,r2,c2 = mv
            print(f"White (AI) {mv}")
        else:
            legal = [m for m,_ in succ(bd)]
            r,c,r2,c2 = random.choice(legal)
            mv = (r,c,r2,c2)
            print(f"Black (rand) {mv}")
        bd[r2][c2], bd[r][c] = bd[r][c], E
        turn_max = not turn_max
    render(bd)
    print("White wins!" if utility(bd) > 0 else "Black wins!")

if __name__ == "__main__":
    play()
