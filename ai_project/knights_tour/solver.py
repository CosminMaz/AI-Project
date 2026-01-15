import io
import time
from contextlib import redirect_stdout
from .algorithms import bfs, dfs, iddfs, simulated_annealing, solve_knights_tour_mrv, calculate_energy

def solve_knights_tour(n_size):
    """Solves the Knight's Tour problem for a given board size using multiple algorithms and compares their performance.

    This function implements and benchmarks several algorithms for solving the Knight's Tour problem:
    - Breadth-First Search (BFS)
    - Depth-First Search (DFS)
    - Iterative Deepening DFS (IDDFS)
    - Simulated Annealing
    - Warnsdorff's rule (a Minimum Remaining Values heuristic)

    For small board sizes (<= 5), it runs the classic search algorithms (BFS, DFS, IDDFS).
    For larger boards, it skips these due to their high complexity and only runs
    Simulated Annealing and Warnsdorff's rule.

    Args:
        n_size (int): The size of the square chessboard (n_size x n_size).
                      The function returns early if n_size is less than 5, as no solution exists.

    Returns:
        str: A detailed report string containing the results of each algorithm, including execution time
             and whether a valid solution was found. For Simulated Annealing, it also reports the "energy"
             of the solution, which corresponds to the number of invalid moves. The report concludes by
             identifying the fastest algorithm that found a valid solution and displaying the solution as a
             numbered board.
    """
    if n_size < 5:
        return "Nu există soluție pentru o tablă mai mică de 5x5."

    results = {}
    output_buffer = io.StringIO()

    with redirect_stdout(output_buffer):
        print(f"Rezolvare Knight's Tour pentru tablă {n_size}x{n_size}...\n")

        # Limităm algoritmii clasici pentru N mare
        LIMIT_CLASSIC = 5

        # --- BFS ---
        if n_size <= LIMIT_CLASSIC:
            print("--- Testare BFS ---")
            start = time.time()
            sol_bfs = bfs(n_size)
            duration = time.time() - start
            results['BFS'] = {'time': duration, 'solution': sol_bfs}
            print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_bfs else 'NU'}")
            print("-" * 20 + "\n")
        else:
            print("--- BFS omis (N prea mare) ---\n")

        # --- DFS ---
        if n_size <= LIMIT_CLASSIC:
            print("--- Testare DFS ---")
            start = time.time()
            sol_dfs = dfs(n_size)
            duration = time.time() - start
            results['DFS'] = {'time': duration, 'solution': sol_dfs}
            print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_dfs else 'NU'}")
            print("-" * 20 + "\n")
        else:
            print("--- DFS omis (N prea mare) ---\n")

        # --- IDDFS ---
        if n_size <= LIMIT_CLASSIC:
            print("--- Testare IDDFS ---")
            start = time.time()
            sol_iddfs = iddfs(n_size)
            duration = time.time() - start
            results['IDDFS'] = {'time': duration, 'solution': sol_iddfs}
            print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_iddfs else 'NU'}")
            print("-" * 20 + "\n")
        else:
            print("--- IDDFS omis (N prea mare) ---\n")

        # --- Simulated Annealing ---
        print("--- Testare Simulated Annealing ---")
        start = time.time()
        sol_sa = simulated_annealing(n_size)
        duration = time.time() - start
        energy = calculate_energy(sol_sa, n_size)
        results['Simulated Annealing'] = {'time': duration, 'solution': sol_sa, 'energy': energy}
        print(f"Timp: {duration:.4f}s. Mutări invalide (Energy): {energy}")
        print("-" * 20 + "\n")

        # --- MRV (Warnsdorff) ---
        print("--- Testare MRV (Warnsdorff) ---")
        start = time.time()
        sol_mrv = solve_knights_tour_mrv(n_size)
        duration = time.time() - start
        results['MRV'] = {'time': duration, 'solution': sol_mrv}
        print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_mrv else 'NU'}")
        print("-" * 20 + "\n")

    # Generare raport
    response = output_buffer.getvalue()
    response += "\n=== Concluzie ===\n"

    valid_algos = {}
    for name, res in results.items():
        if res.get('solution'):
            if name == 'Simulated Annealing' and res['energy'] > 0:
                continue
            valid_algos[name] = res['time']

    if valid_algos:
        fastest = min(valid_algos, key=valid_algos.get)
        response += f"Cel mai rapid algoritm care a găsit o soluție validă este **{fastest}** ({valid_algos[fastest]:.4f}s).\n"
        
        # Formatare soluție ca matrice
        path = results[fastest]['solution']
        board = [[0] * n_size for _ in range(n_size)]
        for i, (r, c) in enumerate(path):
            board[r][c] = i + 1
            
        formatted_sol = ""
        for row in board:
            formatted_sol += " ".join(f"{num:2d}" for num in row) + "\n"
            
        response += f"\nSoluția ({fastest}):\n{formatted_sol}"
    else:
        response += "Niciun algoritm nu a găsit o soluție completă validă."

    return response
