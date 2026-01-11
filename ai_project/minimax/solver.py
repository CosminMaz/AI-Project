
import math

def minimax_alpha_beta(node, depth, alpha, beta, maximizing_player, pruned_nodes):
    """
    Minimax algorithm with Alpha-Beta pruning.
    """
    if depth == 0 or not isinstance(node, list):
        return node, 1

    if maximizing_player:
        max_eval = -math.inf
        visited_nodes = 0
        for child in node:
            evaluation, visited = minimax_alpha_beta(child, depth - 1, alpha, beta, False, pruned_nodes)
            visited_nodes += visited
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                pruned_nodes.append(child)
                break
        return max_eval, visited_nodes
    else:
        min_eval = math.inf
        visited_nodes = 0
        for child in node:
            evaluation, visited = minimax_alpha_beta(child, depth - 1, alpha, beta, True, pruned_nodes)
            visited_nodes += visited
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                pruned_nodes.append(child)
                break
        return min_eval, visited_nodes

def solve_minimax(tree_str):
    """
    Parses a tree from a string and solves it using Minimax with Alpha-Beta pruning.
    """
    try:
        tree = eval(tree_str)
    except:
        return "Error: Invalid tree format."

    pruned_nodes = []
    max_depth = 4 # Assuming a default max depth
    value, visited_nodes = minimax_alpha_beta(tree, max_depth, -math.inf, math.inf, True, pruned_nodes)

    response = f"Minimax with Alpha-Beta Pruning:\n"
    response += f"  - Root Value: {value}\n"
    response += f"  - Visited Leaf Nodes: {visited_nodes}\n"
    response += f"  - Pruned Subtrees (and their children): {pruned_nodes}\n"
    
    return response

if __name__ == '__main__':
    # Example usage:
    # The tree is represented as a nested list.
    # The leaves are numbers.
    tree_string = "[ [5, 6], [7, 4], [8, 9] ]"
    print(solve_minimax(tree_string))

    tree_string_2 = "[ [ [1, 2], [3, 4] ], [ [5, 6], [7, 8] ] ]"
    print(solve_minimax(tree_string_2))
