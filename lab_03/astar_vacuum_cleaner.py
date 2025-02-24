import heapq


# -----------------------------
# Generic A* Search
# -----------------------------

class Node:
    def __init__(self, state, path, cost):
        self.state = state  # Problem-specific state
        self.path = path  # List of actions taken to reach this state
        self.cost = cost  # Cost from start to this node

    def total_cost(self, heuristic):
        """Return f(n) = g(n) + h(n) for the node."""
        return self.cost + heuristic(self.state)

    def __lt__(self, other):
        # The comparison operator for the priority queue based on total cost.
        return self.cost < other.cost


def a_star_search(start_state, goal_test, successors, cost_function, heuristic):
    """
    Generic A* search.

    Args:
        start_state: The initial state.
        goal_test (function): A function that takes a state and returns True if it is a goal.
        successors (function): A function that takes a state and returns an iterable of (action, new_state, step_cost).
        cost_function (function): A function to update the cost given current cost and step cost (typically addition).
        heuristic (function): A function that estimates cost from a state to the goal.

    Returns:
        (path, total_cost, nodes_expanded) if a solution is found, or (None, None, nodes_expanded) otherwise.
    """
    root = Node(start_state, [], 0)
    frontier = []
    heapq.heappush(frontier, (root.total_cost(heuristic), root))
    explored = set()
    nodes_expanded = 0

    while frontier:
        _, current_node = heapq.heappop(frontier)

        # Skip states that have already been explored.
        if current_node.state in explored:
            continue

        explored.add(current_node.state)
        nodes_expanded += 1

        # Check for goal.
        if goal_test(current_node.state):
            return current_node.path, current_node.cost, nodes_expanded

        for action, new_state, step_cost in successors(current_node.state):
            new_cost = cost_function(current_node.cost, step_cost)
            new_node = Node(new_state, current_node.path + [action], new_cost)
            if new_state not in explored:
                heapq.heappush(frontier, (new_node.total_cost(heuristic), new_node))

    return None, None, nodes_expanded


# -----------------------------
# Vacuum Cleaner
# -----------------------------

# Define positions (for a linear environment; could be extended)
POSITIONS = ['A', 'B', 'C', 'D']


def vac_initial_state():
    """
    Return the initial state for the vacuum cleaner.
    State is represented as a tuple:
      (current_position, status_A, status_B, status_C, status_D)
    All positions start as 'Dirty'.
    """
    return ('A', 'Dirty', 'Dirty', 'Dirty', 'Dirty')


def vac_goal_test(state):
    """
    The goal is reached when all positions are 'Clean'.
    """
    return all(status == 'Clean' for status in state[1:])


def vac_successors(state):
    """
    Given a vacuum state, return an iterable of (action, new_state, cost) tuples.
    Allowed actions:
      - 'Suck': Clean the current square if it is dirty.
      - 'Right': Move right if not at the rightmost position.
      - 'Left': Move left if not at the leftmost position.
    Every action has a cost of 1.
    """
    successors = []
    current_pos = state[0]
    pos_index = POSITIONS.index(current_pos)
    statuses = list(state[1:])  # statuses for A, B, C, D

    # Action: Suck (only if current square is Dirty)
    if statuses[pos_index] == 'Dirty':
        new_statuses = statuses.copy()
        new_statuses[pos_index] = 'Clean'
        new_state = (current_pos, *new_statuses)
        successors.append(('Suck', new_state, 1))

    # Action: Right (if not at the rightmost position)
    if current_pos != 'D':
        new_pos = POSITIONS[pos_index + 1]
        new_state = (new_pos, *statuses)
        successors.append(('Right', new_state, 1))

    # Action: Left (if not at the leftmost position)
    if current_pos != 'A':
        new_pos = POSITIONS[pos_index - 1]
        new_state = (new_pos, *statuses)
        successors.append(('Left', new_state, 1))

    return successors


def vac_cost_function(current_cost, step_cost):
    """For the vacuum cleaner, the cost is just cumulative sum of moves."""
    return current_cost + step_cost


def vac_heuristic(state):
    """
    A simple heuristic for the vacuum cleaner: count the number of dirty squares.
    This is admissible because at minimum each dirty square requires one action (Suck).
    """
    return sum(1 for status in state[1:] if status == 'Dirty')


# -----------------------------
# Solve the Vacuum Cleaner Problem using A*
# -----------------------------

def main():
    start = vac_initial_state()
    path, total_cost, nodes_expanded = a_star_search(
        start_state=start,
        goal_test=vac_goal_test,
        successors=vac_successors,
        cost_function=vac_cost_function,
        heuristic=vac_heuristic
    )

    if path is not None:
        print("Solution found!")
        print("Path: " + " -> ".join(path))
        print("Total Cost:", total_cost)
        print("Nodes Expanded:", nodes_expanded)
    else:
        print("No solution found.")


if __name__ == '__main__':
    main()
