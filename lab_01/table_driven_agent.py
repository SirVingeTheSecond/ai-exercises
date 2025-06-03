"""
Lab-01 ▸ Exercise 1  ▸ Table-Driven Vacuum Agent
-------------------------------------------------
• Shows how the percept-history index explodes exponentially
• Answers:
  – Q3: 4 table entries if *only* current percept is used      (2 locations × 2 statuses)
  – Q4: 4**T entries for an agent lifetime of T time-steps     (branching factor = 4)

  - Table-driven agent ⇒ space = O(b^T) -> impractical beyond tiny T.

  - Branching factor here is 4 (A/B × Clean/Dirty).

  - Missing entry ⇒ agent returns None (shows table is incomplete).
"""

# --- constants --------------------------------------------------------------- #
A, B = 'A', 'B'               # ► 2-square world (exam: deterministic env.)

# --- global state ------------------------------------------------------------ #
percepts = []                 # ► history = agent memory for table lookup

# --- finite (incomplete) action table --------------------------------------- #
# Keys are *tuples of percepts*; values are actions.
table = {
    ((A, 'Clean'),): 'Right',
    ((A, 'Dirty'),): 'Suck',
    ((B, 'Clean'),): 'Left',
    ((B, 'Dirty'),): 'Suck',
    # Only a handful of longer histories included -> lookup will fail later
    ((A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left',
}

# --- agent logic ------------------------------------------------------------- #
def LOOKUP(history, tbl):
    """Return action or None  (►None ⇒ missing entry ⇒ table must be enlarged)."""
    return tbl.get(tuple(history))

def TABLE_DRIVEN_AGENT(percept):
    """Core algorithm from AIMA (static table + growing history)."""
    percepts.append(percept)            # 1 ▸ accumulate history
    return LOOKUP(percepts, table)      # 2 ▸ pick action from table

# --- helpers for Q3 & Q4 ----------------------------------------------------- #
def min_entries_single_percept():
    """For |Locations|=2, |Status|=2 ⇒ branching = 4."""
    return 2 * 2                       # small hook: O(b) not O(b^T)

def entries_for_T_steps(T):
    """Exponential blow-up: branching^T with branching=4."""
    return 4 ** T                      # exam: space complexity = b^T

# --- demo run (fulfils Exercise 1 steps) ------------------------------------ #
def run_demo():
    print("Action\t\tPercepts")
    print(TABLE_DRIVEN_AGENT((A, 'Clean')), "\t", percepts)
    print(TABLE_DRIVEN_AGENT((A, 'Dirty')), "\t", percepts)
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), "\t", percepts)

    # Extra call required by exercise (same percept again)
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), "\t", percepts,
          "  <-- None because 4-length history missing")

    # Q3 & Q4 numeric answers
    print("\nQ3 -> entries if only current percept used:\t", min_entries_single_percept())
    T = 4
    print(f"Q4 -> entries for agent-lifetime T={T} steps:\t", entries_for_T_steps(T),
          "(general formula 4**T)")

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    run_demo()
