"""
Lab 02 ▸ Exercise 1 — Uninformed Search Fringe Order
====================================================
Takeaways:
    • **Front‑insert ➜ LIFO ➜ Depth‑First Search**  (stack behaviour)
    • **Rear‑insert  ➜ FIFO ➜ Breadth‑First Search** (queue behaviour)
    • Fringe trace reveals node‑expansion order
    • State‑space size small ⇒ manual tracing feasible.
"""

# -------- search graph (letters A‑J) ----------------------------------------
STATE_SPACE = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [], 'E': [], 'F': [],
    'G': ['H', 'I', 'J'], 'H': [], 'I': [], 'J': []
}
INITIAL_STATE, GOAL_STATE = 'A', 'J'

# -------- search control toggle --------------------------------------------
STRATEGY = 'BFS'  # set to 'BFS' to switch behaviour

# -------- node ----------------------------------------------------------------
class Node:
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

    def path(self):
        n, p = self, []
        while n:
            p.append(n)
            n = n.PARENT_NODE
        return p[::-1]

    def __repr__(self):
        return f"{self.STATE}"

# -------- fringe management --------------------------------------------------

def INSERT(node, queue):
    """Front insert ⇒ DFS  ;  Rear insert ⇒ BFS."""
    if STRATEGY == 'DFS':
        queue.insert(0, node)   # LIFO stack push
    else:
        queue.append(node)      # FIFO enqueue
    return queue


def INSERT_ALL(nodes, queue):
    """Maintain child order while delegating to INSERT."""
    for n in nodes:
        INSERT(n, queue)
    return queue


def REMOVE_FIRST(queue):
    return queue.pop(0)         # always pop front

# -------- helper ------------------------------------------------------------

def successor_fn(state):
    return STATE_SPACE[state]

# -------- main algorithm ----------------------------------------------------

def EXPAND(node):
    children = []
    for s in successor_fn(node.STATE):
        children.append(Node(s, parent=node, depth=node.DEPTH + 1))
    return children


def TREE_SEARCH():
    fringe = INSERT(Node(INITIAL_STATE), [])
    step = 0
    while fringe:
        node = REMOVE_FIRST(fringe)
        print(f"Step {step:>2} | expand {node} | fringe -> {fringe}")
        step += 1
        if node.STATE == GOAL_STATE:
            return node.path()
        fringe = INSERT_ALL(EXPAND(node), fringe)
    return None

# -------- demo --------------------------------------------------------------
if __name__ == '__main__':
    path = TREE_SEARCH()
    print("\nSolution path:", ' -> '.join(n.STATE for n in path))
