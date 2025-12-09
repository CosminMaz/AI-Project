from collections import deque
import heapq
import itertools


# --- STATE REPRESENTATION ---

class NQueensState:
    def __init__(self, queens, n):
        self.queens = queens  # list of row positions
        self.n = n

    def is_goal(self):
        return len(self.queens) == self.n and self.is_valid()

    def is_valid(self):
        for c1 in range(len(self.queens)):
            for c2 in range(c1 + 1, len(self.queens)):
                r1, r2 = self.queens[c1], self.queens[c2]
                if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                    return False
        return True

    def successors(self):
        """Generate all valid next states by adding one more queen."""
        col = len(self.queens)
        if col >= self.n:
            return []
        result = []
        for row in range(self.n):
            new_state = NQueensState(self.queens + [row], self.n)
            if new_state.is_valid():
                result.append(new_state)
        return result

    def __hash__(self):
        return hash(tuple(self.queens))

    def __eq__(self, other):
        return isinstance(other, NQueensState) and self.queens == other.queens and self.n == other.n

    def __repr__(self):
        return f"{self.queens}"


# --- PROBLEM WRAPPER ---

class NQueensProblem:
    def __init__(self, n, algorithm):
        self.initial_state = NQueensState([], n)
        self.algorithm = algorithm  # function reference (e.g., bfs, a_star)

    def solve(self):
        """Solve the problem using the algorithm provided."""
        return self.algorithm(self.initial_state)


# --- SEARCH ALGORITHMS ---

def bfs(start_state):
    frontier = deque([start_state])
    explored = set()

    while frontier:
        state = frontier.popleft()
        if state.is_goal():
            return state
        explored.add(state)
        for child in state.successors():
            if child not in explored and child not in frontier:
                frontier.append(child)
    return None


def dfs(start_state):
    stack = [start_state]
    explored = set()

    while stack:
        state = stack.pop()
        if state.is_goal():
            return state
        explored.add(state)
        for child in state.successors():
            if child not in explored:
                stack.append(child)
    return None


def iddfs(start_state):
    """Iteratively deepen the DFS depth limit."""
    depth = 0
    while True:
        result = dls(start_state, depth)
        if result is not None:
            return result
        depth += 1


def dls(state, limit):
    """Depth-limited search helper for IDDFS."""
    if state.is_goal():
        return state
    if limit == 0:
        return None
    for child in state.successors():
        result = dls(child, limit - 1)
        if result is not None:
            return result
    return None

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

# --- EXAMPLE USAGE ---

if __name__ == "__main__":
    n = 30
    visualizer = NQueensVisualizer(symbols=("♛", "·"))

    algorithms = [
#        ("BFS", bfs),
        ("DFS", dfs),
#        ("IDDFS", iddfs)
    ]

    for name, algorithm in algorithms:
        print(f"\nSolving with {name}:")
        problem = NQueensProblem(n, algorithm)
        solution = problem.solve()

        if solution:
            print("Solution found:", solution)
            visualizer.print_board(solution)
        else:
            print("No solution found.")