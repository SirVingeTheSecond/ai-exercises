"""
Extended Reflex Agent with State (Homework 2)
- Implements a vacuum cleaner agent with internal state
- Tracks environment model across 4 locations
- Demonstrates state-based decision making

Features:
- Four-location environment (A->B->C->D linear arrangement)
- Internal state tracking and environment modeling
- Rule-based action selection
- Protection against invalid actions
- Support for any starting location
"""

A, B, C, D = 'A', 'B', 'C', 'D'

# Initialize environment
Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A  # Can be modified to any starting position (A,B,C,D)
}

# Agent state and model
state = {}
action = None
model = {A: None, B: None, C: None, D: None}  # Track cleanliness of all locations

RULE_ACTION = {
    1: 'Suck',  # Clean dirty square
    2: 'Right',  # Move right
    3: 'Left',  # Move left
    4: 'NoOp'  # Do nothing (all clean)
}

rules = {
    # Basic cleaning rules
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,

    # Movement rules based on location
    (A, 'Clean'): 2,  # Move right from A
    (B, 'Clean'): 2,  # Move right from B
    (C, 'Clean'): 2,  # Move right from C
    (D, 'Clean'): 3,  # Move left from D

    # Terminal state when all locations clean
    (A, B, C, D, 'Clean'): 4
}


def INTERPRET_INPUT(input):
    """
    Process sensor input.

    Args:
        input (tuple): Raw sensor data (location, status)

    Returns:
        tuple: Processed state information
    """
    return input


def RULE_MATCH(state, rules):
    """
    Match current state to appropriate rule.

    Args:
        state: Current state of the environment
        rules (dict): Available rules for action selection

    Returns:
        int: Rule number to apply
    """
    rule = rules.get(tuple(state) if isinstance(state, tuple) else state)
    return rule


def UPDATE_STATE(state, action, percept):
    """
    Update internal state based on percept and model.

    Args:
        state: Current internal state
        action: Last action performed
        percept (tuple): Current sensor reading (location, status)

    Returns:
        Updated internal state
    """
    location, status = percept
    state = percept

    # Update model with new information
    model[location] = status

    # Check if all locations are clean
    if all(model[loc] == 'Clean' for loc in [A, B, C, D]):
        state = (A, B, C, D, 'Clean')

    return state


def REFLEX_AGENT_WITH_STATE(percept):
    """
    Determine action using internal state and rules.

    Args:
        percept (tuple): Current sensor reading

    Returns:
        str: Selected action
    """
    global state, action
    state = UPDATE_STATE(state, action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


def Sensors():
    """
    Return current location and status.

    Returns:
        tuple: (location, status) of current position
    """
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):
    """
    Execute valid actions only, protecting environment integrity.

    Args:
        action (str): Action to perform ('Suck', 'Right', 'Left', 'NoOp')

    Valid transitions:
        - Suck: Cleans current location
        - Right: A->B->C->D
        - Left: D->C->B->A
        - NoOp: No change
    """
    location = Environment['Current']

    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location in [A, B, C]:
        Environment['Current'] = {'A': B, 'B': C, 'C': D}[location]
    elif action == 'Left' and location in [B, C, D]:
        Environment['Current'] = {'B': A, 'C': B, 'D': C}[location]
    # NoOp requires no action


def run(n):
    """
    Run agent for n steps, displaying environment state changes.

    Args:
        n (int): Number of steps to run

    Output format:
        Current location and status
        Action taken
        New location and status after action
    """
    print('    Current                        New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = Sensors()
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_AGENT_WITH_STATE(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20)