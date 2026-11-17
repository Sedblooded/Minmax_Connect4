import random

ROWS = 6
COLS = 8
EMPTY = "_"
PLAYER = "X"
COMPUTER = "O"


def create_board():
    """Columns are stored bottom-to-top: board[col][0] is the bottom cell."""
    return {col: [EMPTY for _ in range(ROWS)] for col in range(COLS)}


def drop_coin(board, coin, col):
    if col not in range(COLS) or EMPTY not in board[col]:
        return False

    for row in range(ROWS):
        if board[col][row] == EMPTY:
            board[col][row] = coin
            return True
    return False


def get_valid_locations(board):
    return [col for col in range(COLS) if EMPTY in board[col]]


def check_winner(board):
    """Return 'X', 'O', or None."""
    directions = ((1, 0), (0, 1), (1, 1), (-1, 1))

    for col in range(COLS):
        for row in range(ROWS):
            coin = board[col][row]
            if coin == EMPTY:
                continue

            for dr, dc in directions:
                cells = []
                for step in range(4):
                    r = row + dr * step
                    c = col + dc * step
                    if not (0 <= r < ROWS and 0 <= c < COLS):
                        break
                    cells.append(board[c][r])

                if len(cells) == 4 and all(cell == coin for cell in cells):
                    return coin
    return None


def board_scoring(board, computer_coin):
    """The supplied window-scoring evaluation, retained for depth-limited search."""
    opponent_coin = "O" if computer_coin == "X" else "X"
    score = 0

    def evaluate_window(window):
        comp_count = window.count(computer_coin)
        opp_count = window.count(opponent_coin)

        if comp_count > 0 and opp_count == 0:
            return {1: 10, 2: 1000, 3: 10000, 4: 100000}[comp_count]
        if opp_count > 0 and comp_count == 0:
            return -{1: 10, 2: 1000, 3: 10000, 4: 100000}[opp_count]
        return 0

    # Vertical windows
    for col in range(COLS):
        for row in range(ROWS - 3):
            score += evaluate_window([board[col][row + i] for i in range(4)])

    # Horizontal windows
    for row in range(ROWS):
        for col in range(COLS - 3):
            score += evaluate_window([board[col + i][row] for i in range(4)])

    # Positive diagonal windows
    for col in range(COLS - 3):
        for row in range(ROWS - 3):
            score += evaluate_window([board[col + i][row + i] for i in range(4)])

    # Negative diagonal windows
    for col in range(COLS - 3):
        for row in range(3, ROWS):
            score += evaluate_window([board[col + i][row - i] for i in range(4)])

    return score


def is_terminal_node(board):
    return check_winner(board) is not None or not get_valid_locations(board)


def alpha_beta_solve(
    board,
    depth,
    alpha=float("-inf"),
    beta=float("inf"),
    isMaxPlayer=True,
    computer_coin=COMPUTER,
):
    valid_locations = get_valid_locations(board)
    winner = check_winner(board)

    # Prefer quicker wins and slower losses within the searched horizon.
    if winner == computer_coin:
        return 100000 + depth, None
    if winner is not None:
        return -100000 - depth, None
    if not valid_locations:
        return 0, None
    if depth == 0:
        return board_scoring(board, computer_coin), None

    opponent_coin = "X" if computer_coin == "O" else "O"

    if isMaxPlayer:
        max_eval = float("-inf")
        best_col = random.choice(valid_locations)

        for col in valid_locations:
            temp_board = {c: values.copy() for c, values in board.items()}
            drop_coin(temp_board, computer_coin, col)

            evaluation, _ = alpha_beta_solve(
                temp_board, depth - 1, alpha, beta, False, computer_coin
            )

            if evaluation > max_eval:
                max_eval, best_col = evaluation, col

            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break

        return max_eval, best_col

    min_eval = float("inf")
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        temp_board = {c: values.copy() for c, values in board.items()}
        drop_coin(temp_board, opponent_coin, col)

        evaluation, _ = alpha_beta_solve(
            temp_board, depth - 1, alpha, beta, True, computer_coin
        )

        if evaluation < min_eval:
            min_eval, best_col = evaluation, col

        beta = min(beta, min_eval)
        if alpha >= beta:
            break

    return min_eval, best_col


def get_ai_move(board, depth=4, computer_coin=COMPUTER):
    score, column = alpha_beta_solve(
        board=board,
        depth=depth,
        alpha=float("-inf"),
        beta=float("inf"),
        isMaxPlayer=True,
        computer_coin=computer_coin,
    )
    return column, score
