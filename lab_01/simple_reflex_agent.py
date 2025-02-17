"""
Simple Reflex Agent
- Uses condition-action rules with dictionaries
- Demonstrates bogus action handling through:
  * Swapped Left/Right movements
  * Invalid actions (Crash, Self-destruct)
- Shows Actuator protection by only allowing valid state transitions
"""

A = 'A'
B = 'B'

# Modified rules and actions to include bogus behaviors
RULE_ACTION = {
    1: 'Suck',
    2: 'Left',  # Bogus (should be Right)
    3: 'Right', # Bogus (should be Left)
    4: 'Crash', # Bogus action
    5: 'Self-destruct' # Bogus action
}

rules = {
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (A, 'Clean'): 2,
    (B, 'Clean'): 3,
    (A, B, 'Clean'): 4,
    (B, B, 'Clean'): 5
}

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    'Current': A
}

def INTERPRET_INPUT(input):
    """Pass through input without interpretation."""
    return input

def RULE_MATCH(state, rules):
    """Match current state to appropriate rule."""
    rule = rules.get(tuple(state))
    return rule

def SIMPLE_REFLEX_AGENT(percept):
    """Determine action using condition-action rules."""
    state = INTERPRET_INPUT(percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action

def Sensors():
    """Return current location and status."""
    location = Environment['Current']
    return (location, Environment[location])

def Actuators(action):
    """Execute valid actions only, protecting environment integrity.
    Invalid actions (Crash, Self-destruct) are ignored.
    Only allows:
    - Suck: Cleans current location
    - Right: A to B movement only
    - Left: B to A movement only"""
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Left' and location == B:
        Environment['Current'] = A

def run(n):
    """Run agent for n steps, displaying environment state changes."""
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = SIMPLE_REFLEX_AGENT(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:8s}{:12s}{:8s}".format(action, location, status))

if __name__ == '__main__':
    run(10)