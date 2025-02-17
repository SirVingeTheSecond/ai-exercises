# Define the state space for the vacuum world problem.
STATE_SPACE = {
    ('A', 'Dirty', 'Dirty'): [('A', 'Clean', 'Dirty'), ('B', 'Dirty', 'Dirty')],
    ('A', 'Clean', 'Dirty'): [('B', 'Clean', 'Dirty')],
    ('B', 'Dirty', 'Dirty'): [('B', 'Clean', 'Dirty'), ('A', 'Dirty', 'Dirty')],
    ('B', 'Dirty', 'Clean'): [('A', 'Dirty', 'Clean')],
    ('A', 'Dirty', 'Clean'): [('A', 'Clean', 'Clean'), ('B', 'Dirty', 'Clean')],
    ('A', 'Clean', 'Clean'): [('B', 'Clean', 'Clean')],
    ('B', 'Clean', 'Dirty'): [('B', 'Clean', 'Clean'), ('A', 'Clean', 'Dirty')],
    ('B', 'Clean', 'Clean'): []
}

INITIAL_STATE = ('A', 'Dirty', 'Dirty')
GOAL_STATE = ('B', 'Clean', 'Clean')

class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)   # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)

'''
Insert node into the queue (fringe).
'''
def INSERT(node, queue):
    queue.append(node)  # Insert at the end (FIFO)
    return queue

'''
Insert list of nodes into the fringe.
'''
def INSERT_ALL(list, queue):
    queue.extend(list)  # Insert list at the end (FIFO)
    return queue

'''
Removes and returns the first element from fringe.
'''
def REMOVE_FIRST(queue):
    return queue.pop(0)  # Remove the first element

'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''
def EXPAND(node):
    successors = []
    children = STATE_SPACE[node.STATE]
    for child in children:
        s = Node(state=child, parent=node, depth=node.DEPTH + 1)
        successors.append(s)
    return successors

'''
Search the tree for the goal state and return path from initial state to goal state
'''
def TREE_SEARCH():
    fringe = []
    explored = set() # Set to keep track of explored states - keep us from entering an infinite loop
    initial_node = Node(state=INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    while fringe:
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE:
            return node.path()
        if node.STATE not in explored:
            explored.add(node.STATE)
            children = EXPAND(node)
            fringe = INSERT_ALL(children, fringe)
        print("Fringe:", fringe)
    return None

'''
Successor function, mapping the nodes to its successors.
'''
def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']

'''
Run tree search and display the nodes in the path to goal node.
'''
def run():
    path = TREE_SEARCH()
    if path:
        print('Solution path:')
        for node in path:
            node.display()
    else:
        print("No solution found")

if __name__ == '__main__':
    run()
