"""
Homework 2 ▸ 4‑Square Reflex Agent with State
=============================================
Takeaways:
    • *Model‑based reflex* ⇒ keeps **internal state** based on percept history
    • Needs a **world model** (how env. evolves + effect of actions) -> handles partial observability
    • Memory cost grows with |locations| (O(n) here) – still lightweight vs. table‑driven O(b^T)
    • Emits **NoOp** once model believes *all four squares are clean* (goal reached)
"""

# ── world constants ───────────────────────────────────────────────────────────
A, B, C, D = 'A', 'B', 'C', 'D'        # 4‑location linear world
VALID_ACTIONS = {'Suck', 'Left', 'Right', 'NoOp'}

# ── environment (mutable) ─────────────────────────────────────────────────────
Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A,                     # ← any starting square allowed
}

# ── internal agent memory ─────────────────────────────────────────────────────
model = {A: None, B: None, C: None, D: None}  # tracks perceived cleanliness
state  = None     # latest abstracted state
action = None     # previous action

# ── rule base (condition -> rule‑id) & actions  ───────────────────────────────
RULE_ACTION = {
    1: 'Suck',     # clean current square
    2: 'Right',    # move right
    3: 'Left',     # move left
    4: 'NoOp',     # do nothing (goal)
}

rules = {
    # cleaning rules
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,

    # movement rules when location already clean
    (A, 'Clean'): 2,
    (B, 'Clean'): 2,
    (C, 'Clean'): 2,
    (D, 'Clean'): 3,

    # terminal condition (all clean)
    (A, B, C, D, 'Clean'): 4,
}

# ── helper functions ──────────────────────────────────────────────────────────

def UPDATE_STATE(state, last_action, percept):
    """Update *model* with newest percept, derive abstract *state*.
    – Exam hook: combines **percept history** + **model of env.**
    """
    loc, status = percept
    model[loc] = status                 # remember cleanliness

    # when model thinks every square clean ⇒ use special composite key
    if all(model[l] == 'Clean' for l in (A, B, C, D)):
        return (A, B, C, D, 'Clean')

    return percept                      # otherwise just use current percept


def RULE_MATCH(state):
    """Return rule‑id or None (missing rule ⇒ undefined)."""
    return rules.get(tuple(state))


def REFLEX_AGENT_WITH_STATE(percept):
    """Model‑based reflex: uses UPDATE_STATE -> RULE_MATCH -> RULE_ACTION."""
    global state, action
    state  = UPDATE_STATE(state, action, percept)
    rule   = RULE_MATCH(state)
    action = RULE_ACTION.get(rule, 'NoOp')
    return action

# ── sensor & actuator interface ──────────────────────────────────────────────

def Sensors():
    loc = Environment['Current']
    return (loc, Environment[loc])


def Actuators(act):
    """Guard environment: ignore commands outside VALID_ACTIONS."""
    if act not in VALID_ACTIONS:
        return                           # bogus ⇒ no state change

    loc = Environment['Current']
    if act == 'Suck':
        Environment[loc] = 'Clean'
    elif act == 'Right' and loc in (A, B, C):
        Environment['Current'] = {A: B, B: C, C: D}[loc]
    elif act == 'Left'  and loc in (B, C, D):
        Environment['Current'] = {B: A, C: B, D: C}[loc]
    # NoOp leaves world untouched

# ── simulation driver ────────────────────────────────────────────────────────

def run(steps: int = 20):
    print('    Current                        New')
    print('location    status  action  location    status')
    for _ in range(steps):
        (loc, st) = Sensors()
        print(f'{loc:12}{st:8}', end='')
        act = REFLEX_AGENT_WITH_STATE(Sensors())
        Actuators(act)
        (new_loc, new_st) = Sensors()
        print(f'{act:8}{new_loc:12}{new_st:8}')

# ── demo ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    run(20)  # expected: clean all squares then enter NoOp idle state
