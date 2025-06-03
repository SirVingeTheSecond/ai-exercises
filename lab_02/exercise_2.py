"""
Lab 02 ▸ Exercise 2 — Vacuum-World via Breadth-First Search
==========================================================
Takeaways:
    • State = (location, A-status, B-status)  → captures **everything** BFS needs
    • Breadth-First Search ⇒ guarantees **shortest action sequence** (optimal cost = #moves)
    • Explored-set prevents revisiting states |V| ≤ 8  (2 locs × 2² dirt configs)
    • Successor fn embodies env. physics:  Suck / Move / NoOp   (exam favourite)
"""

# --- state-space ------------------------------------------------------------- #
# Explicit enumeration keeps code short; 8 reachable states in 2-square world.
STATE_SPACE = {
    ('A', 'Dirty', 'Dirty'): [ ('A', 'Clean', 'Dirty'), ('B', 'Dirty', 'Dirty') ],
    ('A', 'Clean', 'Dirty'): [ ('B', 'Clean', 'Dirty') ],
    ('A', 'Dirty', 'Clean'): [ ('A', 'Clean', 'Clean'), ('B', 'Dirty', 'Clean') ],
    ('A', 'Clean', 'Clean'): [ ('B', 'Clean', 'Clean') ],                # goal on A
    ('B', 'Dirty', 'Dirty'): [ ('B', 'Dirty', 'Clean'), ('A', 'Dirty', 'Dirty') ],
    ('B', 'Clean', 'Dirty'): [ ('B', 'Clean', 'Clean'), ('A', 'Clean', 'Dirty') ],
    ('B', 'Dirty', 'Clean'): [ ('B', 'Clean', 'Clean'), ('A', 'Dirty', 'Clean') ],
    ('B', 'Clean', 'Clean'): []                                           # goal on B
}

INITIAL_STATE = ('B', 'Dirty', 'Dirty')      # sample start
GOAL_STATE    = ('A', 'Clean', 'Clean')      # desired end

# --- node abstraction -------------------------------------------------------- #
class Node:
    def __init__(self, state, parent=None, depth=0):
        self.STATE, self.PARENT_NODE, self.DEPTH = state, parent, depth
    def path(self):
        n, p = self, []
        while n: p.append(n); n = n.PARENT_NODE
        return p[::-1]
    def __repr__(self): return f"{self.STATE}"

# --- fringe ops (BFS) -------------------------------------------------------- #
def INSERT(node, queue):           # rear-insert ⇒ FIFO
    queue.append(node); return queue

def INSERT_ALL(nodes, queue):
    queue.extend(nodes); return queue

def REMOVE_FIRST(queue):           # pop front
    return queue.pop(0)

# --- algorithm -------------------------------------------------------------- #
def EXPAND(node):
    return [Node(s, node, node.DEPTH+1) for s in STATE_SPACE[node.STATE]]

def TREE_SEARCH():
    fringe, explored = INSERT(Node(INITIAL_STATE), []), set()
    step = 0
    while fringe:
        node = REMOVE_FIRST(fringe)
        print(f"Step {step:>2} | expand {node} | fringe → {fringe}"); step += 1
        if node.STATE == GOAL_STATE: return node.path()
        if node.STATE not in explored:
            explored.add(node.STATE)
            INSERT_ALL(EXPAND(node), fringe)
    return None

# --- demo ------------------------------------------------------------------- #
if __name__ == '__main__':
    sol = TREE_SEARCH()
    print("\nSolution path:", ' → '.join(str(n.STATE) for n in sol))
