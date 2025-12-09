class NQueensVisualizer:
    def __init__(self, symbols=("Q", ".")):
        self.symbols = symbols

    def as_matrix(self, state):
        """Return a 2D matrix (list of lists) representing the board from a given NQueensState."""
        n = state.n
        board = [[self.symbols[1] for _ in range(n)] for _ in range(n)]
        for col, row in enumerate(state.queens):
            board[row][col] = self.symbols[0]
        return board

    def print_board(self, state):
        """Pretty-print the board for a given NQueensState."""
        matrix = self.as_matrix(state)
        for row in matrix:
            print(" ".join(row))
        print()


