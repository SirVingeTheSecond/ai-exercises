"""
Lab 02 ▸ Homework — Farmer, Wolf, Goat & Cabbage (BFS)
======================================================
Takeaways:
    • State = (Farmer, Wolf, Goat, Cabbage)  each ∈ {W,E}  → 2⁴ = 16 combos
    • Breadth-First Search guarantees **minimum crossings**
    • `is_valid()` encodes safety constraints; successor_fn filters invalid moves
    • Classic river-crossing shows **search + constraint checking** pattern
"""

# --- helpers ---------------------------------------------------------------- #
def opposite(side):          # switch riverbank
    return 'E' if side == 'W' else 'W'

def is_valid(state):
    _, wolf, goat, cabbage = state
    # Goat with wolf or cabbage without farmer ⇒ invalid
    if wolf == goat and state[0] != goat:   return False
    if goat == cabbage and state[0] != goat:return False
    return True

def successor_fn(state):
    """Generate legal successors (farmer alone or farmer+one)."""
    farmer, wolf, goat, cabbage = state
    moves = [
        (opposite(farmer), wolf, goat, cabbage),                 # farmer only
        (opposite(farmer), opposite(wolf), goat, cabbage)   if farmer==wolf    else None,
        (opposite(farmer), wolf, opposite(goat), cabbage)   if farmer==goat    else None,
        (opposite(farmer), wolf, goat, opposite(cabbage))  if farmer==cabbage else None
    ]
    return [s for s in moves if s and is_valid(s)]

# --- BFS scaffolding -------------------------------------------------------- #
INITIAL_STATE, GOAL_STATE = ('W','W','W','W'), ('E','E','E','E')

class Node:
    def __init__(self, state, parent=None, depth=0):
        self.STATE, self.PARENT_NODE, self.DEPTH = state, parent, depth
    def path(self):
        n,p=self,[];
        while n: p.append(n); n=n.PARENT_NODE
        return p[::-1]
    def __repr__(self): return f"{self.STATE}"

def INSERT(n,q): q.append(n); return q            # BFS rear-insert

def INSERT_ALL(ns,q): q.extend(ns); return q

def REMOVE_FIRST(q): return q.pop(0)

def EXPAND(node):
    return [Node(s,node,node.DEPTH+1) for s in successor_fn(node.STATE)]

def TREE_SEARCH():
    fringe, explored = INSERT(Node(INITIAL_STATE), []), set()
    while fringe:
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE: return node.path()
        if node.STATE not in explored:
            explored.add(node.STATE)
            INSERT_ALL(EXPAND(node), fringe)
    return None

# --- demo ------------------------------------------------------------------- #
if __name__ == "__main__":
    path = TREE_SEARCH()
    print("Solution path:\n",
          " → ".join(str(n.STATE) for n in path) if path else "No solution")
