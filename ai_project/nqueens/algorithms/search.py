from collections import deque

from ai_project.nqueens.algorithms.state import NQueensState


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


