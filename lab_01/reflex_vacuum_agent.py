"""
Exercise 2 ▸ Simple Reflex Vacuum Agent  (2-square world)

▶  Takeaways:
    • Simple-reflex agent ⇒ chooses action from *current* percept only (O(1) memory)
    • Actuator layer is a like safety filter; world updates **only** for valid actions
    • Bogus / unknown actions are ignored ⇒ environment cannot be corrupted
"""

# ── environment constants ───────────────────────────────────────────────────── #
A, B              = 'A', 'B'                     # two locations
VALID_ACTIONS     = {'Suck', 'Left', 'Right'}    # recognised by actuators

# initial world state
Environment = {A: 'Dirty',
               B: 'Dirty',
               'Current': A}  # agent starts on A (change freely for tests)

# toggle to inject bogus behaviour required by step-3 -------------------------- #
BOGUS = True  # False -> correct rules,  True -> deliberately wrong moves

# ── agent definition ────────────────────────────────────────────────────────── #
def REFLEX_VACUUM_AGENT(loc_st):
    """
    Simple reflex: if dirty ⇒ Suck else move.
    When BOGUS=True we purposely swap Left/Right to test actuator protection.
    """
    location, status = loc_st

    # rule 1 – clean current square
    if status == 'Dirty':
        return 'Suck'

    # rule 2 – move according to location
    if not BOGUS:
        # correct behaviour
        return 'Right' if location == A else 'Left'
    else:
        # bogus: intentionally wrong
        return 'Left'  if location == A else 'Right'

# ── sensor & actuator interface ─────────────────────────────────────────────── #
def Sensors():
    """Return (location, status) – percept seen by agent."""
    loc = Environment['Current']
    return (loc, Environment[loc])

def Actuators(action):
    """
    Update world ONLY for valid actions – guards against bogus agent output.
    Valid transitions:
        • Suck  – clean current square
        • Right – move A -> B
        • Left  – move B -> A
    """
    if action not in VALID_ACTIONS:
        return                           # ignore nonsense actions
    loc = Environment['Current']
    if action == 'Suck':
        Environment[loc] = 'Clean'
    elif action == 'Right' and loc == A:
        Environment['Current'] = B
    elif action == 'Left'  and loc == B:
        Environment['Current'] = A
    # any other combination is silently ignored (still a safeguard)

# ── simulation driver ───────────────────────────────────────────────────────── #
def run(steps):
    """Run agent for *steps* iterations, printing world evolution."""
    print('    Current                        New')
    print('location    status  action  location    status')
    for _ in range(steps):
        (loc, st) = Sensors()
        print(f'{loc:12}{st:8}', end='')
        act = REFLEX_VACUUM_AGENT(Sensors())
        Actuators(act)
        (new_loc, new_st) = Sensors()
        print(f'{act:8}{new_loc:12}{new_st:8}')

# ── demo (exercise requires run(10)) ────────────────────────────────────────── #
if __name__ == '__main__':
    run(10)