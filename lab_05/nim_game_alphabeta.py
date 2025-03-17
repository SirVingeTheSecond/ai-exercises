from lab_05.nim_game_minimax import nim_is_terminal, nim_successors, nim_utility


def alpha_beta_decision_nim(state):
    """Selects the best move using alpha–beta pruning for Nim."""
    infinity = float('inf')

    def max_value(state, alpha, beta):
        if nim_is_terminal(state):
            return nim_utility(state)
        v = -infinity
        for (move, succ) in nim_successors(state):
            v = max(v, min_value(succ, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if nim_is_terminal(state):
            return nim_utility(state)
        v = infinity
        for (move, succ) in nim_successors(state):
            v = min(v, max_value(succ, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_move, best_state = max(
        nim_successors(state),
        key=lambda m: min_value(m[1], -infinity, infinity)
    )
    return best_move, best_state

def nim_game_alpha_beta():
    # Start with 20 tokens and MIN to move first.
    state = ([20], "MIN")
    while not nim_is_terminal(state):
        piles, player = state
        print("\nCurrent piles:", piles)
        if player == "MIN":
            # Human move.
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
            move, state = alpha_beta_decision_nim(state)
            print(f"Computer splits pile {move[0]} into {move[1]} and {move[2]}.")
    print("\nFinal piles:", state[0])
    result = nim_utility(state)
    if result == 1:
        print("MAX wins!")
    else:
        print("MIN wins!")

# Uncomment the next line to play the Nim game with alpha–beta pruning:
# nim_game_alpha_beta()
