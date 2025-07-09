import heapq

graph = {
    'A': {'neighbors': {'B': 1, 'C': 2, 'D': 4}, 'h': 6},
    'B': {'neighbors': {'F': 5, 'E': 4}, 'h': 5},
    'C': {'neighbors': {'E': 1}, 'h': 5},
    'D': {'neighbors': {'H': 1, 'I': 4, 'J': 2}, 'h': 2},
    'E': {'neighbors': {'G': 2, 'H': 3}, 'h': 4},
    'F': {'neighbors': {'G': 1}, 'h': 5},
    'G': {'neighbors': {'K': 6}, 'h': 4},
    'H': {'neighbors': {'K': 6, 'L': 5}, 'h': 1},
    'I': {'neighbors': {'L': 3}, 'h': 2},
    'J': {'neighbors': {}, 'h': 1},
    'K': {'neighbors': {}, 'h': 0}, # Goal node
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
        return f'State: {self.STATE} | Cost: {self.PATH_COST} | Heuristic: {self.HEURISTIC}'

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
            state=neighbor,
            parent=node,
            path_cost=new_path_cost,
            heuristic=heuristic,
            f_weight=f_weight if algorithm == 'astar' else 0
        )
        successors.append(s)

    # Print a summary of the expansion
    child_states = ", ".join(child.STATE for child in successors)
    print(f"Expanding '{node.STATE}' -> Children: [{child_states}]")
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

        # When a goal is found, return the full path
        if node.STATE in GOAL_STATES:
            print(f"Goal '{node.STATE}' reached after expanding {nodes_expanded} node(s).")
            return node.path()

        if node.STATE not in explored:
            explored.add(node.STATE)
            nodes_expanded += 1
            children = EXPAND(node, algorithm, f_weight)
            for child in children:
                heapq.heappush(priority_queue, (child.TOTAL_COST, child))
            # Print the current fringe (states only)
            current_fringe = ", ".join(n[1].STATE for n in priority_queue)
            print(f"Current Fringe: [{current_fringe}]\n")

    return None


def format_path(path):
    """
    Formats the final path and total cost for pretty printing.
    """
    path_str = " -> ".join(node.STATE for node in path)
    total_cost = path[-1].PATH_COST if path else 0
    return path_str, total_cost


def run_comparison():
    """
    Runs both Greedy Best-First and A* search algorithms.
    """
    print("-" * 50)
    print(" GREEDY BEST-FIRST SEARCH ".center(50, "-"))
    print("-" * 50)
    greedy_path = INFORMED_SEARCH(algorithm='greedy')
    if greedy_path:
        path_str, total_cost = format_path(greedy_path)
        print("Path Found: " + path_str)
        print("Total Cost: " + str(total_cost))
    else:
        print("No solution found")

    print("\n" + "-" * 50)
    print("    A* SEARCH    ".center(50, "-"))
    print("-" * 50)
    astar_path = INFORMED_SEARCH(algorithm='astar')
    if astar_path:
        path_str, total_cost = format_path(astar_path)
        print("Path Found: " + path_str)
        print("Total Cost: " + str(total_cost))
    else:
        print("No solution found")


if __name__ == '__main__':
    run_comparison()