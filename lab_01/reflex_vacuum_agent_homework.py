"""
Homework 1 - Simple Reflex Vacuum Agent (N‑square linear world)
===========================================================================
Edit **SQUARES** or other constants below to match any exam variation in
seconds.

Variables (all grouped at the top):
    • SQUARES – list of location labels (length ≥ 2)
    • DIRTY_INIT – default status for every square ("Dirty" or "Clean")
    • STEPS – default number of iterations when run from CLI

Everything else (environment dictionaries, movement maps, policy) is
automatically derived from those parameters – no other lines need
editing.
"""

from typing import List, Dict, Tuple

# ── CONFIG ─────────────────────────────────────────────────────────────────
SQUARES: List[str] = ["A", "B", "C", "D"]  # <<< change here for different N
DIRTY_INIT: str = "Dirty"                  # default starting dirt status
VALID_ACTIONS = {"Suck", "Left", "Right"}
STEPS: int = 20                            # demo run length

# ── DERIVED LOOK‑UPS ──────────────────────────────────────────────────────
INDEX: Dict[str, int] = {loc: i for i, loc in enumerate(SQUARES)}

# ── ENVIRONMENT (mutable) ─────────────────────────────────────────────────
Environment: Dict[str, str] = {loc: DIRTY_INIT for loc in SQUARES}
Environment["Current"] = SQUARES[0]  # starting square (edit freely)

# ── I/OLAYERS ────────────────────────────────────────────────────────────

def Sensors() -> Tuple[str, str]:
    """Return current (location, status)."""
    loc = Environment["Current"]
    return loc, Environment[loc]


def Actuators(action: str) -> None:
    """Safely mutate world for **valid** actions; ignore anything else."""
    if action not in VALID_ACTIONS:
        return  # bogus command

    loc = Environment["Current"]
    idx = INDEX[loc]

    if action == "Suck":
        Environment[loc] = "Clean"
    elif action == "Right" and idx < len(SQUARES) - 1:
        Environment["Current"] = SQUARES[idx + 1]
    elif action == "Left" and idx > 0:
        Environment["Current"] = SQUARES[idx - 1]
    # All other combos (e.g., Right on last square) are safely ignored.

# ── AGENT POLICY ──────────────────────────────────────────────────────────

def REFLEX_VACUUM_AGENT(percept: Tuple[str, str]) -> str:
    """Simple‑reflex policy parametric in **SQUARES** list length."""
    loc, status = percept
    if status == "Dirty":
        return "Suck"

    idx = INDEX[loc]
    return "Right" if idx < len(SQUARES) - 1 else "Left"

# ── SIMULATION DRIVER ─────────────────────────────────────────────────────

def run(steps: int = STEPS) -> None:
    """Run agent *steps* iterations and print a compact trace."""
    hdr = "Current                         New"
    sub = "loc      status  act   loc      status"
    print(hdr)
    print(sub)

    for _ in range(steps):
        loc, st = Sensors()
        print(f"{loc:8}{st:8}", end="")
        act = REFLEX_VACUUM_AGENT(Sensors())
        Actuators(act)
        nloc, nst = Sensors()
        print(f"{act:6}{nloc:8}{nst:8}")


# ── ENTRYPOINT ────────────────────────────────────────────────────────
if __name__ == "__main__":
    run()
