import random
import math
import time
from collections import deque

class GraphColoringState:
    def __init__(self, graph, colors, assignment=None):
        self.graph = graph
        self.colors = colors
        self.assignment = assignment if assignment is not None else {}
        self.nodes = list(graph.keys())

    def is_goal(self):
        return len(self.assignment) == len(self.nodes) and self.is_valid()

    def is_valid(self):
        for node, color in self.assignment.items():
            for neighbor in self.graph.get(node, []):
                if neighbor in self.assignment and self.assignment[neighbor] == color:
                    return False
        return True

    def successors(self):
        if len(self.assignment) == len(self.nodes):
            return []
        
        # Select next unassigned node (simple ordering)
        next_node = self.nodes[len(self.assignment)]
        
        children = []
        for color in self.colors:
            new_assignment = self.assignment.copy()
            new_assignment[next_node] = color
            child_state = GraphColoringState(self.graph, self.colors, new_assignment)
            if child_state.is_valid(): # Pruning invalid branches early
                children.append(child_state)
        return children

    def __hash__(self):
        # Convert assignment dict to a sorted tuple of items for hashing
        return hash(tuple(sorted(self.assignment.items())))

    def __eq__(self, other):
        return self.assignment == other.assignment

# --- Search Algorithms ---

def bfs(graph, colors):
    start_state = GraphColoringState(graph, colors)
    if start_state.is_goal(): return start_state.assignment

    frontier = deque([start_state])
    # explored = set() # Optional for tree search structure here, but good for graph search
    
    while frontier:
        state = frontier.popleft()
        if state.is_goal():
            return state.assignment
        
        for child in state.successors():
            frontier.append(child)
    return None

def dfs(graph, colors):
    start_state = GraphColoringState(graph, colors)
    stack = [start_state]
    
    while stack:
        state = stack.pop()
        if state.is_goal():
            return state.assignment
        
        for child in state.successors():
            stack.append(child)
    return None

def iddfs(graph, colors):
    def dls(state, limit):
        if state.is_goal():
            return state.assignment
        if limit == 0:
            return None
        
        for child in state.successors():
            result = dls(child, limit - 1)
            if result is not None:
                return result
        return None

    start_state = GraphColoringState(graph, colors)
    depth = 0
    while True:
        result = dls(start_state, depth)
        if result is not None:
            return result
        depth += 1
        if depth > len(graph): # Optimization: depth cannot exceed number of nodes
            return None

# --- Simulated Annealing ---

def count_conflicts(graph, assignment):
    conflicts = 0
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            if node < neighbor: # Check each edge once
                if assignment.get(node) == assignment.get(neighbor):
                    conflicts += 1
    return conflicts

def simulated_annealing(graph, colors, max_steps=10000, initial_temp=100.0, cooling_rate=0.995):
    nodes = list(graph.keys())
    # Initial random assignment
    current_assignment = {node: random.choice(colors) for node in nodes}
    current_conflicts = count_conflicts(graph, current_assignment)
    
    best_assignment = current_assignment.copy()
    best_conflicts = current_conflicts
    
    temp = initial_temp
    
    for step in range(max_steps):
        if best_conflicts == 0:
            return best_assignment
            
        if temp <= 0.001:
            break

        # Pick a random node and change its color
        node = random.choice(nodes)
        old_color = current_assignment[node]
        new_color = random.choice(colors)
        while new_color == old_color and len(colors) > 1:
            new_color = random.choice(colors)
            
        next_assignment = current_assignment.copy()
        next_assignment[node] = new_color
        next_conflicts = count_conflicts(graph, next_assignment)
        
        delta = next_conflicts - current_conflicts
        
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_assignment = next_assignment
            current_conflicts = next_conflicts
            
            if current_conflicts < best_conflicts:
                best_assignment = current_assignment.copy()
                best_conflicts = current_conflicts
        
        temp *= cooling_rate
        
    return best_assignment # May not be optimal (0 conflicts)

# --- MRV Backtracking ---

def solve_coloring_mrv(graph, colors):
    nodes = list(graph.keys())
    assignment = {}
    
    def get_valid_colors(node, current_assignment):
        valid = set(colors)
        for neighbor in graph.get(node, []):
            if neighbor in current_assignment:
                if current_assignment[neighbor] in valid:
                    valid.remove(current_assignment[neighbor])
        return list(valid)

    def select_unassigned_variable(assignment):
        unassigned = [n for n in nodes if n not in assignment]
        # MRV: node with fewest legal values
        return min(unassigned, key=lambda n: len(get_valid_colors(n, assignment)))

    def backtrack():
        if len(assignment) == len(nodes):
            return assignment
        
        var = select_unassigned_variable(assignment)
        for value in get_valid_colors(var, assignment):
            assignment[var] = value
            result = backtrack()
            if result is not None:
                return result
            del assignment[var]
        return None

    return backtrack()
