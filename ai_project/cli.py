import sys
import argparse

from ai_project.nash import solve_nash_equilibrium
from ai_project.nqueens import generate_response, run_experiment
from ai_project.minimax import solve_minimax
from ai_project.csp import solve_csp_problem
from ai_project.graph_coloring.solver import solve_graph_coloring
from ai_project.knights_tour.solver import solve_knights_tour
from ai_project.hanoi.solver import solve_hanoi


def handle_nqueens():
    """Handles the N-Queens problem."""
    try:
        n_size = int(input("Enter the board size (N): "))
        limit = 8
        final_results = run_experiment(n_size, limit)
        final_text = generate_response(n_size, final_results, limit, f"N-Queens for N={n_size}")
        print("\n" + "=" * 50 + "\n")
        print(final_text)
    except ValueError:
        print("Invalid input. Please enter a number.")

def handle_nash():
    """Handles the Nash equilibrium problem."""
    user_question = input("Enter the game matrix (or leave empty for interactive input): ")
    response = solve_nash_equilibrium(user_question)
    print("\n" + "=" * 50 + "\n")
    print(response)

def handle_minimax():
    """Handles the Minimax problem."""
    tree_str = input("Enter the game tree as a nested list (e.g., [[5, 6], [7, 4]]): ")
    response = solve_minimax(tree_str)
    print("\n" + "=" * 50 + "\n")
    print(response)

def handle_csp():
    """Handles the CSP problem."""
    problem_str = input("Enter the CSP problem (e.g., variables: A, B; domains: 1-3; constraints: A != B): ")
    response = solve_csp_problem(problem_str)
    print("\n" + "=" * 50 + "\n")
    print(response)

def handle_graph_coloring():
    """Handles the Graph Coloring problem."""
    graph_str = input('Enter the graph as a JSON adjacency list (e.g., {"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}): ')
    colors_str = input("Enter the colors (comma-separated, e.g., red, green, blue): ")
    response = solve_graph_coloring(graph_str, colors_str)
    print("\n" + "=" * 50 + "\n")
    print(response)

def handle_knights_tour():
    """Handles the Knight's Tour problem."""
    try:
        n_size = int(input("Enter the board size (N): "))
        response = solve_knights_tour(n_size)
        print("\n" + "=" * 50 + "\n")
        print(response)
    except ValueError:
        print("Invalid input. Please enter a number.")

def handle_hanoi():
    """Handles the Generalized Hanoi problem."""
    try:
        n_disks = int(input("Enter the number of disks: "))
        response = solve_hanoi(n_disks)
        print("\n" + "=" * 50 + "\n")
        print(response)
    except ValueError:
        print("Invalid input. Please enter a number.")




def main():
    """
    Entry point for the console application.
    """
    parser = argparse.ArgumentParser(description="AI Project CLI")
    parser.add_argument("--problem", type=str, help="The problem to solve (nqueens, nash, minimax, csp)")
    parser.add_argument("--n", type=int, help="Board size for N-Queens")
    parser.add_argument("--tree", type=str, help="Game tree for Minimax")
    parser.add_argument("--csp_problem", type=str, help="CSP problem string")
    parser.add_argument("--nash_matrix", type=str, help="Nash equilibrium game matrix")
    parser.add_argument("--graph", type=str, help="Graph for Graph Coloring (JSON adjacency list)")
    parser.add_argument("--colors", type=str, help="Colors for Graph Coloring (comma-separated)")
    parser.add_argument("--knights_tour_size", type=int, help="Board size for Knight's Tour")
    parser.add_argument("--hanoi_disks", type=int, help="Number of disks for Generalized Hanoi")

    args = parser.parse_args()

    if args.problem:
        if args.problem == 'nqueens':
            if args.n:
                final_results = run_experiment(args.n, 8)
                final_text = generate_response(args.n, final_results, 8, f"N-Queens for N={args.n}")
                print(final_text)
            else:
                print("Please provide the board size using --n")
        elif args.problem == 'nash':
            response = solve_nash_equilibrium(args.nash_matrix or "")
            print(response)
        elif args.problem == 'minimax':
            if args.tree:
                response = solve_minimax(args.tree)
                print(response)
            else:
                print("Please provide the game tree using --tree")
        elif args.problem == 'csp':
            if args.csp_problem:
                response = solve_csp_problem(args.csp_problem)
                print(response)
            else:
                print("Please provide the CSP problem string using --csp_problem")
        elif args.problem == 'graph-coloring':
            if args.graph and args.colors:
                response = solve_graph_coloring(args.graph, args.colors)
                print(response)
            else:
                print("Please provide the graph and colors using --graph and --colors")
        elif args.problem == 'knights-tour':
            if args.knights_tour_size:
                response = solve_knights_tour(args.knights_tour_size)
                print(response)
            else:
                print("Please provide the board size using --knights_tour_size")
        elif args.problem == 'hanoi':
            if args.hanoi_disks:
                response = solve_hanoi(args.hanoi_disks)
                print(response)
            else:
                print("Please provide the number of disks using --hanoi_disks")
        sys.exit(0)

    print("Welcome to the AI Project CLI!")
    while True:
        print("\nSelect a problem to solve:")
        print("1. N-Queens")
        print("2. Nash Equilibrium")
        print("3. Minimax")
        print("4. CSP")
        print("5. Graph Coloring")
        print("6. Knight's Tour")
        print("7. Generalized Hanoi")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            handle_nqueens()
        elif choice == '2':
            handle_nash()
        elif choice == '3':
            handle_minimax()
        elif choice == '4':
            handle_csp()
        elif choice == '5':
            handle_graph_coloring()
        elif choice == '6':
            handle_knights_tour()
        elif choice == '7':
            handle_hanoi()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


