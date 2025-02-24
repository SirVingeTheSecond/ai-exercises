import heapq

graph = {
    'A': {'neighbors': {'B': 1, 'C': 2, 'D': 4}, 'h': 6},
    'B': {'neighbors': {'F': 5, 'E': 4}, 'h': 5},
    'C': {'neighbors': {'E': 1}, 'h': 5},
    'D': {'neighbors': {'H': 1, 'I': 1, 'J': 2}, 'h': 2},
    'E': {'neighbors': {'G': 2, 'H': 3}, 'h': 4},
    'F': {'neighbors': {'G': 1}, 'h': 5},
    'G': {'neighbors': {'K': 6}, 'h': 4},
    'H': {'neighbors': {'K': 6, 'L': 5}, 'h': 1},
    'I': {'neighbors': {'L': 3}, 'h': 2},
    'J': {'neighbors': {}, 'h': 1},
    'K': {'neighbors': {}, 'h': 0},  # Goal node
    'L': {'neighbors': {}, 'h': 0}  # Goal node
}

# Goal nodes
GOAL_STATES = ['K', 'L']

class Node:
    """
    Represents a node in the search tree.
    """

    def __init__(self, state, parent=None, path_cost=0, heuristic=0, f_weight=1.0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.PATH_COST = path_cost
        self.HEURISTIC = heuristic
        self.TOTAL_COST = heuristic if f_weight == 0 else path_cost + f_weight * heuristic

    def path(self):
        """
        Constructs the path from the root node to the current node.
        """
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:
            current_node = current_node.PARENT_NODE
            path.append(current_node)
        return path[::-1]

    def __repr__(self):
        return f'State: {self.STATE} - Path Cost: {self.PATH_COST} - Heuristic: {self.HEURISTIC}'

    def __lt__(self, other):
        return self.TOTAL_COST < other.TOTAL_COST


def EXPAND(node, algorithm='astar', f_weight=1.0):
    """
    Expands a node by generating its successors.
    """
    successors = []
    neighbor_data = graph[node.STATE]['neighbors']

    for neighbor, cost in neighbor_data.items():
        new_path_cost = node.PATH_COST + cost
        heuristic = graph[neighbor]['h']

        s = Node(
            state = neighbor,
            parent = node,
            path_cost = new_path_cost,
            heuristic = heuristic,
            f_weight = f_weight if algorithm == 'astar' else 0
        )
        successors.append(s)

    return successors


def INFORMED_SEARCH(start_state='A', algorithm='astar', f_weight=1.0):
    """
    Performs either Greedy Best-First Search or A* Search.
    """
    priority_queue = []
    explored = set()

    h_value = graph[start_state]['h']
    initial_node = Node(state=start_state, heuristic=h_value, f_weight=f_weight if algorithm == 'astar' else 0)
    heapq.heappush(priority_queue, (initial_node.TOTAL_COST, initial_node))

    nodes_expanded = 0

    while priority_queue:
        _, node = heapq.heappop(priority_queue)

        if node.STATE in GOAL_STATES:
            return node.path()

        if node.STATE not in explored:
            explored.add(node.STATE)
            nodes_expanded += 1
            children = EXPAND(node, algorithm, f_weight)

            for child in children:
                heapq.heappush(priority_queue, (child.TOTAL_COST, child))

                print("Fringe:", children)

    return None


def run_comparison():
    """
    Runs both Greedy Best-First and A* search algorithms.
    """
    print("- -- GREEDY BEST - FIRST SEARCH - --")
    greedy_path = INFORMED_SEARCH(algorithm='greedy')
    print([node.STATE for node in greedy_path] if greedy_path else "No solution found")

    print('\n')

    print("- -- A * SEARCH - --")
    astar_path = INFORMED_SEARCH(algorithm='astar')
    print([node.STATE for node in astar_path] if astar_path else "No solution found")

if __name__ == '__main__':
    run_comparison()