from ai_project.nqueens.algorithms.state import NQueensState


class NQueensProblem:
    def __init__(self, n, algorithm):
        self.initial_state = NQueensState([], n)
        self.algorithm = algorithm  # function reference (e.g., bfs, a_star)

    def solve(self):
        """Solve the problem using the algorithm provided."""
        return self.algorithm(self.initial_state)


