"""
MRV-based backtracking solver for N-Queens.
"""


#================COD GENERAT CU CHATGPT-5================
def solve_n_queens_mrv(n):
    board = [-1] * n
    used_rows = set()
    used_main_diag = set()
    used_sec_diag = set()

    # compute valid rows for each column dynamically
    def get_valid_rows(col):
        valid = []
        for row in range(n):
            if (row not in used_rows and
                (row - col) not in used_main_diag and
                (row + col) not in used_sec_diag):
                valid.append(row)
        return valid

    def select_next_column():
        """Select the column with the fewest remaining valid rows (MRV)."""
        min_choices = n + 1
        chosen_col = None
        best_rows = None
        for col in range(n):
            if board[col] == -1:
                choices = get_valid_rows(col)
                if not choices:
                    # no valid positions -> dead end
                    return col, []
                if len(choices) < min_choices:
                    min_choices = len(choices)
                    chosen_col = col
                    best_rows = choices
        return chosen_col, best_rows

    def backtrack(placed=0):
        # ✅ base case: all queens placed
        if placed == n:
            return True

        col, valid_rows = select_next_column()
        if not valid_rows:  # ✅ no valid move, backtrack
            return False

        for row in valid_rows:
            # place
            board[col] = row
            used_rows.add(row)
            used_main_diag.add(row - col)
            used_sec_diag.add(row + col)

            if backtrack(placed + 1):  # ✅ recursive step
                return True

            # undo placement
            board[col] = -1
            used_rows.remove(row)
            used_main_diag.remove(row - col)
            used_sec_diag.remove(row + col)

        return False  # ✅ all rows failed, backtrack

    success = backtrack()
    return board if success else None

#================COD GENERAT CU CHATGPT-5================


