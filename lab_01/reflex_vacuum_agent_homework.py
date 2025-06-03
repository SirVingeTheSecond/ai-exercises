"""
Homework 1 ▸ 4-Square Simple Reflex Vacuum Agent
================================================
Takeaways:
    • Simple-reflex ⇒ uses **current percept only** → O(1) memory
    • 4 locations (A-B-C-D linear) ⇒ branch factor still small (Left/Right/Suck)
    • Actuator layer ≈ **gate-keeper** → ignores illegal moves, preserving model
    • Any starting square allowed; test with run(20) for full sweep
"""

# ── world constants ───────────────────────────────────────────────────────────
A, B, C, D = 'A', 'B', 'C', 'D'          # ► 4-square environment
VALID_ACTIONS = {'Suck', 'Left', 'Right'}

# ── environment state (mutable) ───────────────────────────────────────────────
Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A,                        # ← change freely for other tests
}

# ── simple-reflex policy ──────────────────────────────────────────────────────
def REFLEX_VACUUM_AGENT(percept):
    """
    Policy:
        1. If dirty ⇒ Suck
        2. Else move Right while in A/B/C, Left while in D          # greedy sweep
    """
    location, status = percept

    # rule 1 – clean if dirty
    if status == 'Dirty':
        return 'Suck'

    # rule 2 – deterministic sweep
    if location in (A, B, C):
        return 'Right'
    if location == D:
        return 'Left'

# ── sensors & actuators ──────────────────────────────────────────────────────
def Sensors():
    """Return current (location, status)."""
    loc = Environment['Current']
    return (loc, Environment[loc])

def Actuators(action):
    """
    Perform *safe* world updates only; ignore actions outside VALID_ACTIONS.
    Valid transitions:
        • Suck  – cleans current square
        • Right – A→B, B→C, C→D
        • Left  – D→C, C→B, B→A
    Anything else is silently discarded  ➔ integrity check.
    """
    if action not in VALID_ACTIONS:
        return                                      # bogus → ignored

    loc = Environment['Current']
    if action == 'Suck':
        Environment[loc] = 'Clean'
    elif action == 'Right' and loc in (A, B, C):
        Environment['Current'] = {A: B, B: C, C: D}[loc]
    elif action == 'Left' and loc in (B, C, D):
        Environment['Current'] = {B: A, C: B, D: C}[loc]
    # Other combinations (e.g., Right from D) are rejected automatically

# ── simulation driver ────────────────────────────────────────────────────────
def run(steps: int = 20):
    """Run agent *steps* iterations and print trace (location/status changes)."""
    print('    Current                        New')
    print('location    status  action  location    status')
    for _ in range(steps):
        (loc, st) = Sensors()
        print(f'{loc:12}{st:8}', end='')
        act = REFLEX_VACUUM_AGENT(Sensors())
        Actuators(act)
        (new_loc, new_st) = Sensors()
        print(f'{act:8}{new_loc:12}{new_st:8}')

# ── self-test ────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    run(20)      # ► expected: full A→B→C→D→C→B→A sweep while cleaning
