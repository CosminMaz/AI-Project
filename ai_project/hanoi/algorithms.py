import time
import math
import random
from collections import deque
import heapq

class HanoiState:
    """Represents a state in the Tower of Hanoi puzzle.

    Attributes:
        pegs (tuple): A tuple of tuples, where each inner tuple represents a peg
                      and contains the disks on that peg in ascending order from bottom to top.
        n_disks (int): The total number of disks in the puzzle.
    """
    def __init__(self, pegs, n_disks):
        """Initializes a new HanoiState.

        Args:
            pegs (tuple): The configuration of disks on the pegs.
            n_disks (int): The total number of disks.
        """
        # pegs: tuple of tuples, e.g., ((3, 2, 1), (), ())
        self.pegs = pegs
        self.n_disks = n_disks

    def is_goal(self):
        """Checks if the current state is the goal state.

        The goal state is when all disks are on the last peg.

        Returns:
            bool: True if the current state is the goal state, False otherwise.
        """
        # Goal: all disks on the last peg (index 2)
        return len(self.pegs[2]) == self.n_disks

    def successors(self):
        """Generates all valid successor states from the current state.

        A move is valid if the target peg is empty or the top disk on the target peg
        is larger than the disk being moved.

        Returns:
            list: A list of tuples, where each tuple contains a successor state (HanoiState)
                  and the move (disk, source_peg, destination_peg) that led to it.
        """
        children = []
        for i in range(3):
            if not self.pegs[i]:
                continue
            
            disk = self.pegs[i][-1]
            
            for j in range(3):
                if i == j:
                    continue
                
                # Valid move: target peg empty or top disk larger than moving disk
                if not self.pegs[j] or self.pegs[j][-1] > disk:
                    new_pegs = list(list(p) for p in self.pegs)
                    new_pegs[i].pop()
                    new_pegs[j].append(disk)
                    
                    # Convert back to tuple of tuples for immutability/hashing
                    new_pegs_tuple = tuple(tuple(p) for p in new_pegs)
                    children.append((HanoiState(new_pegs_tuple, self.n_disks), (disk, i, j)))
        return children

    def __hash__(self):
        """Computes the hash of the state.

        The hash is based on the configuration of the pegs.

        Returns:
            int: The hash of the state.
        """
        return hash(self.pegs)

    def __eq__(self, other):
        """Checks if two states are equal.

        Two states are equal if their peg configurations are the same.

        Args:
            other (HanoiState): The other state to compare with.

        Returns:
            bool: True if the states are equal, False otherwise.
        """
        return self.pegs == other.pegs
    
    def __lt__(self, other):
        """A dummy less-than method needed for the priority queue in case of equal costs.

        Args:
            other (HanoiState): The other state to compare with.

        Returns:
            bool: Always returns False.
        """
        return False # Needed for priority queue if costs are equal

# --- Search Algorithms ---

def bfs(n_disks):
    """Solves the Tower of Hanoi puzzle using Breadth-First Search (BFS).

    BFS explores the state space layer by layer, guaranteeing that the first solution
    found is the optimal one (i.e., has the minimum number of moves). However, it can
    be memory-intensive.

    Args:
        n_disks (int): The number of disks in the puzzle.

    Returns:
        list: A list of moves representing the solution path, or None if no solution
              is found within the search limit.
    """
    initial_pegs = (tuple(range(n_disks, 0, -1)), (), ())
    start_state = HanoiState(initial_pegs, n_disks)
    
    if start_state.is_goal(): return []

    frontier = deque([(start_state, [])])
    explored = {start_state}
    
    MAX_NODES = 100000
    nodes = 0

    while frontier:
        state, path = frontier.popleft()
        nodes += 1
        if nodes > MAX_NODES: return None

        if state.is_goal():
            return path
        
        for child, move in state.successors():
            if child not in explored:
                explored.add(child)
                new_path = path + [move]
                frontier.append((child, new_path))
    return None

def dfs(n_disks):
    """Solves the Tower of Hanoi puzzle using Depth-First Search (DFS).

    DFS explores as far as possible along each branch before backtracking. It is not
    guaranteed to find the optimal solution and can get trapped in long paths.

    Args:
        n_disks (int): The number of disks in the puzzle.

    Returns:
        list: A list of moves representing the solution path, or None if no solution
              is found within the search limit.
    """
    initial_pegs = (tuple(range(n_disks, 0, -1)), (), ())
    start_state = HanoiState(initial_pegs, n_disks)
    
    stack = [(start_state, [])]
    explored = {start_state}
    
    MAX_NODES = 100000
    nodes = 0

    while stack:
        state, path = stack.pop()
        nodes += 1
        if nodes > MAX_NODES: return None # Prune

        if state.is_goal():
            return path
        
        for child, move in state.successors():
            if child not in explored:
                explored.add(child)
                new_path = path + [move]
                stack.append((child, new_path))
    return None

def iddfs(n_disks):
    """Solves the Tower of Hanoi puzzle using Iterative Deepening DFS (IDDFS).

    IDDFS combines the benefits of DFS (low memory usage) and BFS (optimal solutions)
    by performing a series of depth-limited searches. It is guaranteed to find the
    optimal solution.

    Args:
        n_disks (int): The number of disks in the puzzle.

    Returns:
        list: A list of moves representing the optimal solution path, or None if no
              solution is found within the maximum depth limit.
    """
    initial_pegs = (tuple(range(n_disks, 0, -1)), (), ())
    start_state = HanoiState(initial_pegs, n_disks)

    def dls(state, path, limit, visited):
        if state.is_goal():
            return path
        if limit == 0:
            return None
        
        visited.add(state)
        
        for child, move in state.successors():
            if child not in visited:
                result = dls(child, path + [move], limit - 1, visited)
                if result is not None:
                    return result
        
        visited.remove(state) # Backtrack
        return None

    depth = 0
    max_depth = 2**n_disks + 5 # Optimal is 2^n - 1
    
    while depth <= max_depth:
        visited = set()
        result = dls(start_state, [], depth, visited)
        if result is not None:
            return result
        depth += 1
    return None

# --- Simulated Annealing ---

def heuristic(state):
    """Calculates a heuristic cost for a given state.

    The heuristic is designed to guide the search towards the goal state. A lower
    heuristic cost indicates that a state is closer to the solution.

    The cost is calculated as the sum of 2^k for each disk k that is not on the
    target peg. This gives a higher penalty to larger disks that are misplaced.

    Args:
        state (HanoiState): The state to evaluate.

    Returns:
        int: The heuristic cost of the state.
    """
    # Cost = sum(2^k * dist_to_target)
    # If disk k is on target (peg 2), cost 0.
    # If disk k is on source/aux, cost 2^k.
    cost = 0
    for peg_idx, peg in enumerate(state.pegs):
        for disk in peg:
            if peg_idx != 2: # Not on target peg
                cost += 2 ** (disk - 1)
    return cost

def simulated_annealing(n_disks, max_steps=10000):
    """Solves the Tower of Hanoi puzzle using Simulated Annealing.

    Simulated Annealing is a probabilistic technique for approximating the global
    optimum of a given function. It is a metaheuristic, which means it makes few
    assumptions about the problem and can search a large space of candidate solutions.

    The algorithm starts with a high "temperature" and gradually "cools down". At each
    step, it randomly selects a neighbor of the current state and decides whether to

    move to it based on the change in "energy" (heuristic cost) and the current
    temperature.

    Args:
        n_disks (int): The number of disks in the puzzle.
        max_steps (int, optional): The maximum number of steps to run the algorithm for.
                                 Defaults to 10000.

    Returns:
        list: A list of moves representing the solution path, or None if no solution
              is found within the given number of steps. The solution is not guaranteed
              to be optimal.
    """
    initial_pegs = (tuple(range(n_disks, 0, -1)), (), ())
    current_state = HanoiState(initial_pegs, n_disks)
    current_cost = heuristic(current_state)
    
    path = [] # We only track the path taken, SA doesn't guarantee shortest path
    
    temp = 100.0
    cooling_rate = 0.99
    
    for step in range(max_steps):
        if current_state.is_goal():
            return path
            
        if temp <= 0.01:
            # Restart or break? Let's break.
            break
            
        neighbors = current_state.successors()
        if not neighbors:
            break
            
        # Pick random neighbor
        next_state, move = random.choice(neighbors)
        next_cost = heuristic(next_state)
        
        delta = next_cost - current_cost
        
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_state = next_state
            current_cost = next_cost
            path.append(move)
            
        temp *= cooling_rate
        
    return None # Failed to find solution

# --- Recursive Optimal (Standard Algorithm) ---
# This serves as our "MRV" equivalent (most efficient standard approach)

def solve_hanoi_recursive(n_disks):
    """Solves the Tower of Hanoi puzzle using the standard recursive algorithm.

    This is the classic, optimal solution for the Tower of Hanoi puzzle. It is
    provided here as a baseline for comparison with the other algorithms.

    Args:
        n_disks (int): The number of disks in the puzzle.

    Returns:
        list: A list of moves representing the optimal solution path.
    """
    moves = []
    def move(n, source, target, auxiliary):
        """Recursively moves n disks from the source peg to the target peg.

        Args:
            n (int): The number of disks to move.
            source (int): The index of the source peg.
            target (int): The index of the target peg.
            auxiliary (int): The index of the auxiliary peg.
        """
        if n == 1:
            moves.append((1, source, target))
            return
        move(n - 1, source, auxiliary, target)
        moves.append((n, source, target))
        move(n - 1, auxiliary, target, source)
        
    # Map peg indices 0, 1, 2 to names/indices
    move(n_disks, 0, 2, 1)
    
    # Convert to format (disk, from_idx, to_idx)
    return moves
