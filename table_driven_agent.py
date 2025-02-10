A = 'A'
B = 'B'
percepts = []
table = {
    ((A, 'Clean'),): 'Right',
    ((A, 'Dirty'),): 'Suck',
    ((B, 'Clean'),): 'Left',
    ((B, 'Dirty'),): 'Suck',
    ((A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Dirty')): 'Suck',
    # ...
    ((A, 'Clean'), (A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left',
    # ...
}


def LOOKUP(percepts, table):  # Lookup appropriate action for percepts
    action = table.get(tuple(percepts))
    # In Python 3.6 this does not work, but the following does
    # action = table.get((percepts,))
    return action


def TABLE_DRIVEN_AGENT(percept):  # Determine action based on table and percepts
    percepts.append(percept)  # Add percept
    action = LOOKUP(percepts, table)  # Lookup appropriate action for percepts
    return action


def run():  # run agent on several sequential percepts
    #print('Action\tPercepts')
    #print(TABLE_DRIVEN_AGENT((A, 'Clean')), '\t', percepts)
    #print(TABLE_DRIVEN_AGENT((A, 'Dirty')), '\t', percepts)
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts)
    #print(TABLE_DRIVEN_AGENT((B, 'Dirty')), '\t', percepts)


if __name__ == '__main__':
    run()
