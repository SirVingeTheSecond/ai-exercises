def winner(state):
    wins = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]
    for (i, j, k) in wins:
        if state[i] == state[j] == state[k] and state[i] in ["X", "O"]:
            return state[i]
    return None

def minmax_decision(state):
    infinity = float('inf')

    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    """
    returns True if the state is either a win or a tie (board full)
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    return winner(state) is not None or all(isinstance(s, str) for s in state)


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    w = winner(state)
    if w == "X":
        return 1
    elif w == "O":
        return -1
    else:
        return 0

def successors_of(state):
    """
    returns a list of tuples (move, state) as shown in the exercise slides
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """
    # Determine whose turn it is:
    # X goes first; if the counts are equal, it is X's turn, otherwise it is O's.
    countX = sum(1 for s in state if s == "X")
    countO = sum(1 for s in state if s == "O")
    player = "X" if countX == countO else "O"

    succ = []
    for i, s in enumerate(state):
        if s != "X" and s != "O": # This is an available square (integer)
            new_state = state.copy()
            new_state[i] = player
            succ.append((i, new_state))
    return succ

def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            valid_move = False
            while not valid_move:
                move = input('Your move? ')
                try:
                    move = int(move)
                    # Check if the move is valid: available square equals its index
                    if board[move] == move:
                        board[move] = "O"
                        valid_move = True
                    else:
                        print("Invalid move, bozo. You try again, ye?")
                except (ValueError, IndexError):
                    print("Invalid input, bozo. You try again, ye?")
    display(board)
    print("Game Over!")
    result = utility_of(board)
    if result == 1:
        print("X wins!")
    elif result == -1:
        print("O wins!")
    else:
        print("Draw!")


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
