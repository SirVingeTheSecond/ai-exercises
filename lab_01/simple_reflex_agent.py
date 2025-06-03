"""
Exercise 3 ▸ Simple Reflex Agent (dictionary rules)

Takeaways
-------------------------------------------------
• *Simple‑reflex* ⇒ decision uses **current percept only** → O(1) memory
• Condition‑action **rules table** replaces huge percept table
• Actuator layer = **safety filter** → ignores illegal / bogus actions
• Demonstrates that an *untrusted* agent cannot corrupt environment
"""

# ── world constants ───────────────────────────────────────────────────────────
A, B = 'A', 'B'                   # 2‑location vacuum world
VALID_ACTIONS = {'Suck', 'Left', 'Right'}

# ── environment ──────────────────────────────────────────────────────────────
Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A,                # agent starts on A (change for experiments)
}

# ── rule base (includes bogus mappings on purpose) ───────────────────────────
#   rules  ▸ maps **condition**→rule‑id
#   RULE_ACTION ▸ maps rule‑id → action
#   Some actions are deliberately wrong (e.g. 'Crash') for step‑3 test.
RULE_ACTION = {
    1: 'Suck',        # correct – clean square
    2: 'Left',        # bogus – should move Right from A
    3: 'Right',       # bogus – should move Left  from B
    4: 'Crash',       # invalid – not recognised by actuators
    5: 'Self‑destruct' # invalid – not recognised by actuators
}

rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 3,
    # Non‑sense composite states to trigger bogus actions below
    (A, B, 'Clean'): 4,
    (B, B, 'Clean'): 5,
}

# ── agent implementation ─────────────────────────────────────────────────────

def INTERPRET_INPUT(percept):
    return percept                # pass‑through (simple env.)


def RULE_MATCH(state):
    """Return matching rule‑id or None (no default rule)."""
    return rules.get(tuple(state))


def SIMPLE_REFLEX_AGENT(percept):
    state = INTERPRET_INPUT(percept)         # ① translate percept
    rule = RULE_MATCH(state)                 # ② pick rule
    return RULE_ACTION.get(rule, 'NoOp')     # ③ map to action

# ── sensors & actuators ──────────────────────────────────────────────────────

def Sensors():
    loc = Environment['Current']
    return (loc, Environment[loc])


def Actuators(action):
    """Mutate world only for *valid* actions – guards integrity."""
    if action not in VALID_ACTIONS:
        return                         # ignore bogus commands silently

    loc = Environment['Current']
    if action == 'Suck':
        Environment[loc] = 'Clean'
    elif action == 'Right' and loc == A:
        Environment['Current'] = B
    elif action == 'Left' and loc == B:
        Environment['Current'] = A
    # Any illegal move combination is ignored (additional safeguard)

# ── simulation driver ────────────────────────────────────────────────────────

def run(steps: int = 10):
    """Run agent *steps* iterations and print trace."""
    print('    Current                        New')
    print('location    status  action  location    status')

    for _ in range(steps):
        (loc, st) = Sensors()
        print(f'{loc:12}{st:8}', end='')
        act = SIMPLE_REFLEX_AGENT(Sensors())  # choose action
        Actuators(act)
        (new_loc, new_st) = Sensors()
        print(f'{act:8}{new_loc:12}{new_st:8}')

# ── demo (exercise expects run(10)) ──────────────────────────────────────────
if __name__ == '__main__':
    run(10)