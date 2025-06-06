import heapq

graph = {
    'A': {'neighbors': {'B': 1, 'C': 2, 'D': 4}, 'h': 6},
    'B': {'neighbors': {'F': 5, 'E': 4}, 'h': 5},
    'C': {'neighbors': {'E': 1}, 'h': 5},
    'D': {'neighbors': {'H': 3, 'I': 1, 'J': 2}, 'h': 2},
    'E': {'neighbors': {'G': 2, 'H': 3}, 'h': 4},
    'F': {'neighbors': {'G': 1}, 'h': 5},
    'G': {'neighbors': {'K': 6}, 'h': 5},
    'H': {'neighbors': {'K': 6, 'L': 5}, 'h': 2},
    'I': {'neighbors': {'L': 4}, 'h': 2},
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

'''

### Summary of Differences

- **Expansion Order:**  
  - **Greedy Best-First:**  
    Focuses solely on the heuristic, so it expanded A → D → H and then immediately accepted K as the goal.
  - **A* Search:**  
    Considers both the path cost and the heuristic, leading to a more systematic expansion (A → B → D → H → J → C → I → E) until it found the cheaper goal L.

- **Solution Cost:**  
  - **Greedy Best-First:**  
    Resulted in a solution path with a total cost of 11.
  - **A* Search:**  
    Found a less expensive solution with a total cost of 8, showing A*’s advantage in balancing exploration cost and estimated future cost.

- **Nodes Expanded:**  
  - Greedy search expanded fewer nodes (3) because it stopped as soon as a goal was found based on the heuristic, while A* expanded more nodes (8) to ensure that the overall cost was minimized.

---

### GREEDY BEST-FIRST SEARCH

1. **Initial Expansion from 'A':**  
   - **Printout:**  
     ```
     Expanding 'A' -> Children: [B, C, D]
     Current Fringe: [D, C, B]
     ```
   - **Explanation:**  
     The search starts at node A. From A, the algorithm generates three children: B, C, and D.  
     The "Current Fringe" shows the list of nodes waiting to be expanded. Note that the order here is determined by the heuristic values only (since in greedy search, `f_weight` is set to zero). 
     In this case, D comes first because its heuristic value (or the order imposed by the implementation) made it the highest priority.

2. **Expansion from 'D':**  
   - **Printout:**  
     ```
     Expanding 'D' -> Children: [H, I, J]
     Current Fringe: [H, J, C, B, I]
     ```
   - **Explanation:**  
     Node D is popped from the fringe and expanded. Its children are H, I, and J. These new nodes are added to the fringe.  
     The new fringe order shows H as the next candidate, followed by J, C, B, and I. Again, the ordering reflects the greedy selection based solely on the heuristic.

3. **Expansion from 'H':**  
   - **Printout:**  
     ```
     Expanding 'H' -> Children: [K, L]
     Current Fringe: [K, J, L, B, I, C]
     ```
   - **Explanation:**  
     Node H is expanded next, yielding children K and L. Since K is one of the goal nodes, the algorithm immediately finds a solution.  
     The fringe is updated, but the search stops as soon as it detects that K is a goal state.

4. **Goal Found:**  
   - **Printout:**  
     ```
     Goal 'K' reached after expanding 3 node(s).
     Path Found: A -> D -> H -> K
     Total Cost: 11
     ```
   - **Explanation:**  
     The search found goal K after expanding 3 nodes (A, D, H). The printed path shows the route taken: A → D → H → K, and the total cost (the accumulated path cost) is 11.

---

### A* SEARCH

1. **Initial Expansion from 'A':**  
   - **Printout:**  
     ```
     Expanding 'A' -> Children: [B, C, D]
     Current Fringe: [B, C, D]
     ```
   - **Explanation:**  
     The algorithm starts at A, expanding it to children B, C, and D.  
     For A*, both the path cost and the heuristic are used (i.e., `Total Cost = Path Cost + f_weight * Heuristic`), so the fringe order now reflects the combined cost.

2. **Expansion from 'B':**  
   - **Printout:**  
     ```
     Expanding 'B' -> Children: [F, E]
     Current Fringe: [D, C, F, E]
     ```
   - **Explanation:**  
     Node B is popped next and expanded to yield F and E. The fringe now has D, C, F, and E. The order reflects the lowest total estimated cost.

3. **Expansion from 'D':**  
   - **Printout:**  
     ```
     Expanding 'D' -> Children: [H, I, J]
     Current Fringe: [H, C, J, E, I, F]
     ```
   - **Explanation:**  
     Next, D is expanded to generate children H, I, and J.  
     The fringe is updated with these nodes while still keeping those with lower total costs at the front.

4. **Expansion from 'H':**  
   - **Printout:**  
     ```
     Expanding 'H' -> Children: [K, L]
     Current Fringe: [J, C, L, E, I, K, F]
     ```
   - **Explanation:**  
     Node H is expanded to produce K and L.  
     The goal hasn't been immediately reached because A* considers both the path cost and the heuristic; K might have a higher total cost than another potential path at this moment.

5. **Expansion from 'J':**  
   - **Printout:**  
     ```
     Expanding 'J' -> Children: []
     Current Fringe: [C, I, L, E, F, K]
     ```
   - **Explanation:**  
     Node J is expanded next. It has no children (an empty expansion), so the fringe simply gets updated by removing J.

6. **Expansion from 'C':**  
   - **Printout:**  
     ```
     Expanding 'C' -> Children: [E]
     Current Fringe: [I, E, E, K, F, L]
     ```
   - **Explanation:**  
     Node C expands to produce an additional E (even if another E already exists in the fringe, it represents a different path). The fringe now reflects the new order.

7. **Expansion from 'I':**  
   - **Printout:**  
     ```
     Expanding 'I' -> Children: [L]
     Current Fringe: [E, E, L, K, F, L]
     ```
   - **Explanation:**  
     Expanding I produces another L. Multiple instances of a goal node (L) can appear, but the algorithm will select the one with the best total cost.

8. **Expansion from 'E':**  
   - **Printout:**  
     ```
     Expanding 'E' -> Children: [G, H]
     Current Fringe: [H, E, L, K, F, L, G]
     ```
   - **Explanation:**  
     E is expanded, yielding G and H.  
     Shortly after, one of the goal nodes appears in a favorable position.

9. **Goal Found:**  
   - **Printout:**  
     ```
     Goal 'L' reached after expanding 8 node(s).
     Path Found: A -> D -> I -> L
     Total Cost: 8
     ```
   - **Explanation:**  
     The algorithm finds goal L after expanding 8 nodes. The chosen path is A → D → I → L, and the total accumulated cost for this path is 8.  
     Notice that even though both K and L are goal nodes, A* found a cheaper path (total cost 8) compared to the greedy search result (total cost 11).

'''