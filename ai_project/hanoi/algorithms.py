import time
import math
import random
from collections import deque
import heapq

class HanoiState:
    def __init__(self, pegs, n_disks):
        # pegs: tuple of tuples, e.g., ((3, 2, 1), (), ())
        self.pegs = pegs
        self.n_disks = n_disks

    def is_goal(self):
        # Goal: all disks on the last peg (index 2)
        return len(self.pegs[2]) == self.n_disks

    def successors(self):
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
        return hash(self.pegs)

    def __eq__(self, other):
        return self.pegs == other.pegs
    
    def __lt__(self, other):
        return False # Needed for priority queue if costs are equal

# --- Search Algorithms ---

def bfs(n_disks):
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
    moves = []
    def move(n, source, target, auxiliary):
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
