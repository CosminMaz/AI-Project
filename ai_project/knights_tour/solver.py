def is_valid_move(x, y, board, n):
    """
    Checks if a move is valid.

    A move is valid if it is within the board boundaries and the
    destination square has not been visited yet.

    Args:
        x (int): The x-coordinate of the move.
        y (int): The y-coordinate of the move.
        board (list): The chessboard.
        n (int): The size of the board.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1

def get_onward_moves(x, y, board, n):
    """
    Returns the number of possible onward moves from a square.

    This function is used by Warnsdorff's rule to decide which
    square to move to next.

    Args:
        x (int): The x-coordinate of the square.
        y (int): The y-coordinate of the square.
        board (list): The chessboard.
        n (int): The size of the board.

    Returns:
        int: The number of possible onward moves.
    """
    count = 0
    for move_x, move_y in MOVES:
        if is_valid_move(x + move_x, y + move_y, board, n):
            count += 1
    return count

def solve_knights_tour_util(board, n, curr_x, curr_y, move_count):
    """
    Recursive utility function to solve the Knight's Tour problem.

    This function uses backtracking and Warnsdorff's rule to find a
    solution.

    Args:
        board (list): The chessboard.
        n (int): The size of the board.
        curr_x (int): The current x-coordinate of the knight.
        curr_y (int): The current y-coordinate of the knight.
        move_count (int): The current move number.

    Returns:
        bool: True if a solution is found, False otherwise.
    """
    board[curr_x][curr_y] = move_count

    if move_count == n * n:
        return True

    # Aplică euristica Warnsdorff
    next_moves = []
    for move_x, move_y in MOVES:
        next_x, next_y = curr_x + move_x, curr_y + move_y
        if is_valid_move(next_x, next_y, board, n):
            onward_moves = get_onward_moves(next_x, next_y, board, n)
            next_moves.append((onward_moves, next_x, next_y))
    
    # Sortează mutările posibile în funcție de numărul de continuări
    next_moves.sort()

    for _, next_x, next_y in next_moves:
        if solve_knights_tour_util(board, n, next_x, next_y, move_count + 1):
            return True

    # Backtrack
    board[curr_x][curr_y] = -1
    return False

def solve_knights_tour(n_size):
    """
    Solves the Knight's Tour problem for a board of size N x N.

    Args:
        n_size (int): The size of the board.

    Returns:
        str: A message containing the solution or an error message.
    """
    if n_size < 5:
        return "Nu există soluție pentru o tablă mai mică de 5x5."
        
    board = [[-1 for _ in range(n_size)] for _ in range(n_size)]
    
    # Pozițiile posibile de start ale calului
    global MOVES
    MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1),
             (-2, -1), (-1, -2), (1, -2), (2, -1)]

    # Încearcă să pornească de la (0, 0)
    if solve_knights_tour_util(board, n_size, 0, 0, 1):
        # Formatează soluția pentru afișare
        formatted_solution = ""
        for row in board:
            formatted_solution += " ".join(f"{num:2d}" for num in row) + "\n"
        return f"Soluție găsită pentru Turul Calului pe o tablă de {n_size}x{n_size}:\n\n{formatted_solution}"
    else:
        return f"Nu s-a găsit o soluție pentru Turul Calului pe o tablă de {n_size}x{n_size} pornind de la (0,0)."
