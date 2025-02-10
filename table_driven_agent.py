"""
Table-Driven Agent Implementation
- Demonstrates table lookup based on percept history
- Shows exponential growth of required table entries with time steps
"""

A = 'A'
B = 'B'
percepts = []


'''
This table contains limited entries for demonstration
Full table would need 4^T entries for T time steps
'''
table = {
    ((A, 'Clean'),): 'Right',
    ((A, 'Dirty'),): 'Suck',
    ((B, 'Clean'),): 'Left',
    ((B, 'Dirty'),): 'Suck',
    ((A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left',
}

def LOOKUP(percepts, table):
    """Look up appropriate action for percept sequence."""
    action = table.get(tuple(percepts))
    return action

def TABLE_DRIVEN_AGENT(percept):
    """Determine action based on table and percept history."""
    percepts.append(percept)
    action = LOOKUP(percepts, table)
    return action

def run():
    """Run agent to demonstrate percept history and actions."""
    print('Action\tPercepts')
    print(TABLE_DRIVEN_AGENT((A, 'Clean')), '\t', percepts)
    print(TABLE_DRIVEN_AGENT((A, 'Dirty')), '\t', percepts)
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts)

if __name__ == '__main__':
    run()