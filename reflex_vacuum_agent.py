"""
Extended Reflex Vacuum Agent (Homework 1)
- Implements a vacuum cleaner agent with 4 locations
- Uses simple reflex architecture without state
- Demonstrates movement patterns and cleaning behavior

Features:
- Four-location environment (A->B->C->D linear arrangement)
- Local sensing (agent only knows current location status)
- Reactive behavior based on current percepts
- Protection against invalid actions
- Support for any starting location
"""

A, B, C, D = 'A', 'B', 'C', 'D'

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': A  # Can be modified to any starting position (A,B,C,D)
}

def REFLEX_VACUUM_AGENT(loc_st):
    """
    Determine action based on current location and status.

    Args:
        loc_st (tuple): Current (location, status) perception
            location: One of A,B,C,D indicating current position
            status: 'Clean' or 'Dirty' indicating square's status

    Returns:
        str: Action to take ('Suck', 'Right', 'Left')

    Strategy:
        - Clean current location if dirty
        - Move right when at A,B,C
        - Move left when at D
        - Creates a systematic movement pattern: A->B->C->D->C->B->A
    """
    location, status = loc_st

    if status == 'Dirty':
        return 'Suck'

    # Movement logic for 4-location environment
    if location == A:
        return 'Right'
    if location == B:
        return 'Right'
    if location == C:
        return 'Right'
    if location == D:
        return 'Left'

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
        action (str): Action to perform ('Suck', 'Right', 'Left')

    Valid transitions:
        - Suck: Cleans current location
        - Right: A->B->C->D
        - Left: D->C->B->A
    """
    location = Environment['Current']

    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location in [A, B, C]:
        Environment['Current'] = {'A': B, 'B': C, 'C': D}[location]
    elif action == 'Left' and location in [B, C, D]:
        Environment['Current'] = {'B': A, 'C': B, 'D': C}[location]

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
        action = REFLEX_VACUUM_AGENT(Sensors())
        Actuators(action)
        (location, status) = Sensors()
        print("{:8s}{:12s}{:8s}".format(action, location, status))

if __name__ == '__main__':
    run(20)