# ----------------------------
# Nim Game using Minimax
# ----------------------------

def nim_is_terminal(state):
    """A Nim state is terminal if no pile has 3 or more tokens."""
    piles, player = state
    return all(pile < 3 for pile in piles)

def nim_utility(state):
    """
    In a terminal state, the current player cannot move and loses.
    Return +1 if MAX wins and -1 if MIN wins.
    """
    piles, player = state
    if nim_is_terminal(state):
        # If it's MAX's turn and no move exists, MAX loses.
        if player == "MAX":
            return -1
        else:
            return 1
    return 0

def nim_successors(state):
    """
    Generate all legal moves for Nim.
    For each pile that can be split (pile >= 3), try every split (i from 1 to pile-1)
    where the two parts are not equal. Return a list of (move, new_state) tuples.
    A move is represented as (index, part1, part2), where index is the position
    of the chosen pile.
    """
    piles, player = state
    successors = []
    for idx, pile in enumerate(piles):
        if pile >= 3:
            for i in range(1, pile):
                j = pile - i
                if i != j:  # split must produce piles of different sizes
                    # Remove the chosen pile and add the two new piles.
                    new_piles = piles[:idx] + piles[idx+1:] + [i, j]
                    new_piles.sort()  # sort to keep state canonical
                    # Switch turn.
                    next_player = "MAX" if player == "MIN" else "MIN"
                    new_state = (new_piles, next_player)
                    move = (idx, i, j)
                    successors.append((move, new_state))
    return successors

# We can now re-use the minmax_decision function from our tic-tac-toe code.
def argmax(iterable, func):
    return max(iterable, key=func)

def nim_minmax_decision(state):
    """Selects the best move for the current state using minimax search."""
    infinity = float('inf')

    def max_value(state):
        if nim_is_terminal(state):
            return nim_utility(state)
        v = -infinity
        for (move, succ) in nim_successors(state):
            v = max(v, min_value(succ))
        return v

    def min_value(state):
        if nim_is_terminal(state):
            return nim_utility(state)
        v = infinity
        for (move, succ) in nim_successors(state):
            v = min(v, max_value(succ))
        return v

    best_move, best_state = argmax(nim_successors(state), lambda m: min_value(m[1]))
    return best_move, best_state

# A simple interactive game loop for Nim using minimax:
def nim_game_minmax():
    # Start with 15 tokens and MIN to move first.
    state = ([15], "MIN")
    while not nim_is_terminal(state):
        piles, player = state
        print("\nCurrent piles:", piles)
        if player == "MIN":
            # Human move: show legal moves and prompt for input.
            moves = nim_successors(state)
            print("Legal moves:")
            for index, (move, new_state) in enumerate(moves):
                print(f"{index}: Split pile {move[0]} into {move[1]} and {move[2]}")
            try:
                choice = int(input("Your move (enter move number): "))
                move, state = moves[choice]
            except (ValueError, IndexError):
                print("Invalid input. Try again.")
                continue
        else:
            # Computer (MAX) uses minimax to select a move.
            move, state = nim_minmax_decision(state)
            print(f"Computer splits pile {move[0]} into {move[1]} and {move[2]}.")
    # Game is over.
    print("\nFinal piles:", state[0])
    result = nim_utility(state)
    if result == 1:
        print("MAX wins!")
    else:
        print("MIN wins!")

# Uncomment the next line to play the Nim game with minimax:
# nim_game_minmax()
