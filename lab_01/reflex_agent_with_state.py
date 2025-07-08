"""
Homework 2 — Parametric Model‑Based Reflex Vacuum Agent (N‑square linear world)
===============================================================================
This agent maintains an **internal model** of every square’s cleanliness.
Change the constants under CONFIG to adapt instantly to exam variants
(e.g., different number of squares, new labels, pre‑clean squares).

Key tweak points:
    • SQUARES – ordered list of location labels.
    • DIRTY_INIT – default external dirt status.
    • STEPS – default simulation length.

Policy overview:
    1. Update internal `model` with current percept.
    2. If current square dirty → "Suck".
    3. Else if any square dirty → move one step toward *nearest* dirty square.
    4. Else → "NoOp" (all clean).

The helper `nearest_dirty()` makes the logic invariant to the number of squares.
"""

from typing import List, Dict, Tuple, Optional

# ── CONFIG ─────────────────────────────────────────────────────────────────
SQUARES: List[str] = ["A", "B", "C", "D"]  # <‑‑ Edit for different N / labels
DIRTY_INIT: str = "Dirty"                      # default external dirt status
STEPS: int = 20                                # default run length
VALID_ACTIONS = {"Suck", "Left", "Right", "NoOp"}

# ── DERIVED LOOK‑UPS ──────────────────────────────────────────────────────
INDEX: Dict[str, int] = {loc: i for i, loc in enumerate(SQUARES)}

# ── ENVIRONMENT (mutable) ─────────────────────────────────────────────────
Environment: Dict[str, str] = {loc: DIRTY_INIT for loc in SQUARES}
Environment["Current"] = SQUARES[0]  # starting square (feel free to change)

# ── I/O ────────────────────────────────────────────────────────────

def Sensors() -> Tuple[str, str]:
    """Return (location, status)."""
    loc = Environment["Current"]
    return loc, Environment[loc]


def Actuators(action: str) -> None:
    """Safely mutate world for **valid** actions; ignore anything else."""
    if action not in VALID_ACTIONS:
        return

    loc = Environment["Current"]
    idx = INDEX[loc]

    if action == "Suck":
        Environment[loc] = "Clean"
    elif action == "Right" and idx < len(SQUARES) - 1:
        Environment["Current"] = SQUARES[idx + 1]
    elif action == "Left" and idx > 0:
        Environment["Current"] = SQUARES[idx - 1]
    # "NoOp" leaves world unchanged.

# ── AGENT INTERNAL MODEL & POLICY ─────────────────────────────────────────

# Start with an *unknown* (assumed DIRTY_INIT) model.
model: Dict[str, str] = {loc: DIRTY_INIT for loc in SQUARES}


def nearest_dirty(cur_idx: int) -> Optional[int]:
    """Return index of closest dirty square to *cur_idx*; None if all clean."""
    dirty_indices = [i for i, loc in enumerate(SQUARES) if model[loc] == "Dirty"]
    if not dirty_indices:
        return None
    return min(dirty_indices, key=lambda i: abs(i - cur_idx))


def MODEL_BASED_AGENT(percept: Tuple[str, str]) -> str:
    """Model‑based reflex agent parametric in **SQUARES** length."""
    loc, status = percept

    # 1) Update internal model with current percept.
    model[loc] = status

    # 2) If current square dirty ⇒ Suck.
    if status == "Dirty":
        return "Suck"

    # 3) Otherwise move toward nearest remaining dirty square.
    idx = INDEX[loc]
    target_idx = nearest_dirty(idx)
    if target_idx is None:
        return "NoOp"  # all squares clean

    return "Right" if target_idx > idx else "Left"

# ── SIMULATION DRIVER ─────────────────────────────────────────────────────

def run(steps: int = STEPS) -> None:
    """Run agent *steps* iterations and print a compact trace."""
    hdr = "Current                         New     ModelDirty?"
    sub = "loc      status  act   loc      status  remaining"
    print(hdr)
    print(sub)

    for _ in range(steps):
        loc, st = Sensors()
        dirty_left = sum(1 for s in model.values() if s == "Dirty")
        print(f"{loc:8}{st:8}", end="")
        act = MODEL_BASED_AGENT(Sensors())
        Actuators(act)
        nloc, nst = Sensors()
        print(f"{act:6}{nloc:8}{nst:8}{dirty_left:6}")


# ── ENTRYPOINT ────────────────────────────────────────────────────────
if __name__ == "__main__":
    run()
