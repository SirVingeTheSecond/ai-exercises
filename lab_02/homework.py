# Define the state space for the Farmer, Wolf, Goat, and Cabbage problem.
# Each state is represented as a tuple.
# 'W' = West, 'E' = East.

# (Farmer, Wolf, Goat, Cabbage)
STATE_SPACE = {
    ('W', 'W', 'W', 'W'): [('E', 'W', 'W', 'W'), ('E', 'E', 'W', 'W')],
    ('E', 'W', 'W', 'W'): [('W', 'W', 'W', 'W')],
    ('E', 'E', 'W', 'W'): [('W', 'E', 'W', 'W'), ('E', 'E', 'E', 'W')],
    ('W', 'E', 'W', 'W'): [('E', 'E', 'W', 'W')],
    ('E', 'E', 'E', 'W'): [('W', 'E', 'E', 'W'), ('E', 'E', 'E', 'E')],
    ('W', 'E', 'E', 'W'): [('E', 'E', 'E', 'W')],
    ('E', 'E', 'E', 'E'): []  # Goal state - no further actions needed
}

# Define the initial and goal states
INITIAL_STATE = ('W', 'W', 'W', 'W')  # Everyone starts on the west side
GOAL_STATE = ('E', 'E', 'E', 'E')  # Everyone reaches the east side safely

class Node:
    """
    Represents a node in the search tree.

    Attributes:
        STATE (tuple): The current state (Farmer, Wolf, Goat, Cabbage).
        PARENT_NODE (Node): Reference to the parent node (used for path reconstruction).
        DEPTH (int): Depth of the node in the search tree.
    """

    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):
        """
        Constructs the path from the root node to the current node.

        Returns:
            list: A list of nodes representing the path from the initial state to this node.
        """
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:
            current_node = current_node.PARENT_NODE
            path.append(current_node)
        return path[::-1]  # Reverse to get correct order

    def display(self):
        """Prints a representation of the node to the console."""
        print(self)

    def __repr__(self):
        """Returns a string representation of the node's state and depth."""
        return f'State: {self.STATE} - Depth: {self.DEPTH}'


def INSERT(node, queue):
    """
    Inserts a node into the queue (FIFO behavior for BFS).

    Args:
        node (Node): The node to insert.
        queue (list): The BFS queue.

    Returns:
        list: Updated queue with the new node.
    """
    queue.append(node)  # BFS inserts at the end (FIFO)
    return queue


def INSERT_ALL(list_of_nodes, queue):
    """
    Inserts a list of nodes into the queue.

    Args:
        list_of_nodes (list): List of nodes to be inserted.
        queue (list): The BFS queue.

    Returns:
        list: Updated queue with the new nodes.
    """
    queue.extend(list_of_nodes)  # BFS inserts at the end (FIFO)
    return queue


def REMOVE_FIRST(queue):
    """
    Removes and returns the first element from the queue.

    Args:
        queue (list): The BFS queue.

    Returns:
        Node: The first node in the queue.
    """
    return queue.pop(0)  # BFS removes from the front (FIFO)


def EXPAND(node):
    """
    Expands a node by generating its successors.

    Args:
        node (Node): The node to expand.

    Returns:
        list: A list of successor nodes.
    """
    successors = []
    children = successor_fn(node.STATE)  # Get valid successor states
    for child in children:
        s = Node(state=child, parent=node, depth=node.DEPTH + 1)
        successors.append(s)
    return successors


def TREE_SEARCH():
    """
    Performs Breadth-First Search (BFS) to find a path to the goal state.

    Returns:
        list: A list of nodes from the initial state to the goal state, or None if no solution exists.
    """
    fringe = []  # The queue used for BFS
    explored = set()  # Set to track visited states and avoid loops
    initial_node = Node(state=INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)

    while fringe:
        node = REMOVE_FIRST(fringe)  # Get the first node (FIFO)

        # Check if the current node is the goal state
        if node.STATE == GOAL_STATE:
            return node.path()

        if node.STATE not in explored:
            explored.add(node.STATE)  # Mark node as explored
            children = EXPAND(node)  # Generate successors
            fringe = INSERT_ALL(children, fringe)  # Add successors to the queue

        print("Fringe:", fringe)  # Debugging output

    return None  # No solution found


def is_valid(state):
    """
    Checks if the given state is valid (i.e., no one gets eaten).

    Rules:
    - The goat and wolf cannot be left alone without the farmer.
    - The goat and cabbage cannot be left alone without the farmer.

    Args:
        state (tuple): The (Farmer, Wolf, Goat, Cabbage) locations.

    Returns:
        bool: True if the state is valid, False otherwise.
    """
    _, wolf, goat, cabbage = state

    # Goat gets eaten by wolf
    if wolf == goat and goat != state[0]:
        return False

    # Goat eats the cabbage
    if goat == cabbage and goat != state[0]:
        return False

    return True


def successor_fn(state):
    """
    Generates valid successor states by moving the farmer and at most one passenger.

    Args:
        state (tuple): Current state (Farmer, Wolf, Goat, Cabbage).

    Returns:
        list: A list of valid successor states.
    """
    successors = []
    farmer, wolf, goat, cabbage = state

    # Possible moves (Farmer alone or with one passenger)
    moves = [
        (opposite(farmer), wolf, goat, cabbage),  # Farmer moves alone
        (opposite(farmer), opposite(wolf), goat, cabbage) if farmer == wolf else None,  # Move wolf
        (opposite(farmer), wolf, opposite(goat), cabbage) if farmer == goat else None,  # Move goat
        (opposite(farmer), wolf, goat, opposite(cabbage)) if farmer == cabbage else None  # Move cabbage
    ]

    # Filter valid states
    for new_state in moves:
        if new_state and is_valid(new_state):
            successors.append(new_state)

    return successors


def opposite(side):
    """Returns the opposite riverbank ('W' -> 'E' or 'E' -> 'W')."""
    return 'E' if side == 'W' else 'W'


def run():
    """
    Runs BFS search and displays the solution path if found.
    """
    path = TREE_SEARCH()
    if path:
        print('Solution path:')
        for node in path:
            node.display()
    else:
        print("No solution found")


if __name__ == '__main__':
    run()
