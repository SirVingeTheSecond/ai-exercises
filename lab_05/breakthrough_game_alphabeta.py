def breakthrough_initial_board():
    """Creates an 8x8 board with MAX's pawns on rows 0-1 and MIN's on rows 6-7."""
    board = [[" " for _ in range(8)] for _ in range(8)]
    # MAX: "X" on rows 0 and 1.
    for r in range(2):
        for c in range(8):
            board[r][c] = "X"
    # MIN: "O" on rows 6 and 7.
    for r in range(6, 8):
        for c in range(8):
            board[r][c] = "O"
    return board


def breakthrough_is_terminal(state):
    """Returns True if the game is over."""
    board, player = state
    # Check if a pawn has reached the opponent's home row:
    # MAX wins if an "X" is in row 7; MIN wins if an "O" is in row 0.
    if "X" in board[7] or "O" in board[0]:
        return True
    # Also terminal if a player has no pieces.
    max_exists = any("X" in row for row in board)
    min_exists = any("O" in row for row in board)
    if not max_exists or not min_exists:
        return True
    return False


def breakthrough_utility(state):
    """
    Returns +1 if MAX wins and -1 if MIN wins.
    """
    board, player = state
    # Winning by reaching the opponent's home row:
    if "X" in board[7]:
        return 1
    if "O" in board[0]:
        return -1
    # If one side has no pieces:
    if not any("X" in row for row in board):
        return -1
    if not any("O" in row for row in board):
        return 1
    return 0


def breakthrough_successors(state):
    """
    Generate all legal moves for the current player.
    A pawn moves one step forward or diagonally forward.
    For MAX ("X"), forward means increasing row index.
    For MIN ("O"), forward means decreasing row index.
    A pawn may move diagonally forward onto an empty square or capture an opponent's pawn.
    Returns a list of (move, new_state) pairs.
    A move is represented as ((from_row, from_col), (to_row, to_col)).
    """
    board, player = state
    successors = []
    # Determine the forward direction.
    dr = 1 if player == "X" else -1
    next_player = "O" if player == "X" else "X"
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                moves = []
                # Straight forward:
                nr = r + dr
                if 0 <= nr < 8:
                    if board[nr][c] == " ":
                        moves.append((nr, c))
                # Diagonal left:
                nc = c - 1
                nr = r + dr
                if 0 <= nr < 8 and 0 <= nc < 8:
                    # Allowed if the square is empty or holds an opponent's pawn.
                    if board[nr][nc] == " " or board[nr][nc] != player:
                        moves.append((nr, nc))
                # Diagonal right:
                nc = c + 1
                nr = r + dr
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if board[nr][nc] == " " or board[nr][nc] != player:
                        moves.append((nr, nc))
                for (nr, nc) in moves:
                    new_board = [row.copy() for row in board]
                    # Move the pawn.
                    new_board[nr][nc] = player
                    new_board[r][c] = " "
                    move = ((r, c), (nr, nc))
                    successors.append((move, (new_board, next_player)))
    return successors


# A generic alpha–beta decision function for breakthrough:
def alpha_beta_decision_breakthrough(state):
    infinity = float('inf')

    def max_value(state, alpha, beta):
        if breakthrough_is_terminal(state):
            return breakthrough_utility(state)
        v = -infinity
        for move, succ in breakthrough_successors(state):
            v = max(v, min_value(succ, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if breakthrough_is_terminal(state):
            return breakthrough_utility(state)
        v = infinity
        for move, succ in breakthrough_successors(state):
            v = min(v, max_value(succ, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_move, best_state = max(
        breakthrough_successors(state),
        key=lambda m: min_value(m[1], -infinity, infinity)
    )
    return best_move, best_state


# A simple game loop for Breakthrough:
def breakthrough_game():
    board = breakthrough_initial_board()
    # Let MAX ("X") start.
    state = (board, "X")
    while not breakthrough_is_terminal(state):
        board, player = state
        # Display the board.
        print("\nCurrent board:")
        for row in board:
            print(" ".join(row))
        if player == "X":
            # Computer uses alpha-beta search.
            move, state = alpha_beta_decision_breakthrough(state)
            print(f"Computer (X) moves from {move[0]} to {move[1]}")
        else:
            # Human plays as MIN ("O").
            moves = breakthrough_successors(state)
            print("Legal moves:")
            for i, (move, new_state) in enumerate(moves):
                print(f"{i}: from {move[0]} to {move[1]}")
            try:
                choice = int(input("Your move (enter move number): "))
                move, state = moves[choice]
            except (ValueError, IndexError):
                print("Invalid input. Try again.")
                continue
    # Game over.
    print("\nFinal board:")
    for row in state[0]:
        print(" ".join(row))
    result = breakthrough_utility(state)
    if result == 1:
        print("MAX (X) wins!")
    elif result == -1:
        print("MIN (O) wins!")
    else:
        print("Draw!")

# Uncomment the next line to play Breakthrough:
# breakthrough_game()
