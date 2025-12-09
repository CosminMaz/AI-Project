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


