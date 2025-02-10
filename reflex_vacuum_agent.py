"""
Reflex Vacuum Agent
- Demonstrates simple reflex behavior with bogus actions
- Shows how Actuators protect environment integrity
"""

"""
Running Exercise 2 with bogus actions:
- Agent attempts wrong directions but Actuators prevent invalid moves
- Environment state remains consistent
- Agent still accomplishes cleaning task despite incorrect actions
"""

A = 'A'
B = 'B'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}

def REFLEX_VACUUM_AGENT(loc_st):
    """Determine action based on current location and status.
    Tests bogus actions to demonstrate Actuator protection.

    Returns:
        str: Action to take ('Suck', 'Left', 'Right')
        Note: Returns incorrect directions to test Actuator safety
    """
    if loc_st[1] == 'Dirty':
        return 'Suck'
    if loc_st[0] == A:
        return 'Left'  # Bogus action (should be Right)
    if loc_st[0] == B:
        return 'Right'  # Bogus action (should be Left)

def Sensors():
    """Return current location and status of the environment."""
    location = Environment['Current']
    return (location, Environment[location])

def Actuators(action):
    """Execute actions while protecting environment integrity.
    Only allows valid transitions:
    - Suck: Cleans current location
    - Right: Only works from A to B
    - Left: Only works from B to A

    Invalid actions are silently ignored, preserving environment state.
    """
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Left' and location == B:
        Environment['Current'] = A

def run(n):
    """Run agent for n steps, displaying state changes.
    Shows how bogus actions are handled safely."""
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_VACUUM_AGENT(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:8s}{:12s}{:8s}".format(action, location, status))