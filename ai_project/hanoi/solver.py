import io
import time
from contextlib import redirect_stdout
from .algorithms import bfs, dfs, iddfs, simulated_annealing, solve_hanoi_recursive

PEGS = {0: 'A', 1: 'B', 2: 'C'}
"""A dictionary that maps peg indices to their names."""

def format_moves(moves):
    """Formats a list of moves into a human-readable string.

    Args:
        moves (list): A list of tuples, where each tuple represents a move
                      and contains the disk number, source peg, and destination peg.

    Returns:
        str: A formatted string describing the sequence of moves.
    """
    if not moves:
        return "Nicio mutare."
    return "\n".join([f"- Mută discul {disk} de la {PEGS[src]} la {PEGS[dest]}" for disk, src, dest in moves])

def solve_hanoi(n_disks):
    """Solves the Tower of Hanoi problem for a given number of disks using multiple algorithms 
    and compares their performance.

    This function implements and benchmarks several algorithms for solving the Tower of Hanoi puzzle:
    - Breadth-First Search (BFS)
    - Depth-First Search (DFS)
    - Iterative Deepening DFS (IDDFS)
    - Simulated Annealing
    - The optimal recursive solution

    For a small number of disks (<= 4), it runs all the search algorithms. For a larger number of disks,
    it skips the search algorithms that are too slow (BFS, DFS, IDDFS) and only runs Simulated Annealing
    and the optimal recursive solution.

    Args:
        n_disks (int): The number of disks to solve for. Must be at least 1.

    Returns:
        str: A detailed report string containing the results of each algorithm, including execution time,
             whether a solution was found, and the number of moves. It also includes a conclusion
             that summarizes which algorithm was the fastest and the solution it found.
    """
    if n_disks < 1:
        return "Numărul de discuri trebuie să fie cel puțin 1."

    results = {}
    output_buffer = io.StringIO()

    with redirect_stdout(output_buffer):
        print(f"Rezolvare Hanoi pentru {n_disks} discuri...\n")

        # Limităm algoritmii de căutare. 
        # IDDFS este extrem de lent pentru N >= 5 din cauza re-expandării masive în grafuri cu cicluri.
        # BFS/DFS merg rezonabil până la N=5 sau 6, dar consumă multă memorie.
        LIMIT_SEARCH = 4 

        # --- BFS ---
        if n_disks <= LIMIT_SEARCH:
            print("--- Testare BFS ---")
            start = time.time()
            sol_bfs = bfs(n_disks)
            duration = time.time() - start
            results['BFS'] = {'time': duration, 'solution': sol_bfs}
            print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_bfs is not None else 'NU'}")
            if sol_bfs: print(f"Număr mutări: {len(sol_bfs)}")
            print("-" * 20 + "\n")
        else:
            print(f"--- BFS omis (N > {LIMIT_SEARCH}) ---\n")

        # --- DFS ---
        if n_disks <= LIMIT_SEARCH:
            print("--- Testare DFS ---")
            start = time.time()
            sol_dfs = dfs(n_disks)
            duration = time.time() - start
            results['DFS'] = {'time': duration, 'solution': sol_dfs}
            print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_dfs is not None else 'NU'}")
            if sol_dfs: print(f"Număr mutări: {len(sol_dfs)}")
            print("-" * 20 + "\n")
        else:
            print(f"--- DFS omis (N > {LIMIT_SEARCH}) ---\n")

        # --- IDDFS ---
        if n_disks <= LIMIT_SEARCH:
            print("--- Testare IDDFS ---")
            start = time.time()
            sol_iddfs = iddfs(n_disks)
            duration = time.time() - start
            results['IDDFS'] = {'time': duration, 'solution': sol_iddfs}
            print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_iddfs is not None else 'NU'}")
            if sol_iddfs: print(f"Număr mutări: {len(sol_iddfs)}")
            print("-" * 20 + "\n")
        else:
            print(f"--- IDDFS omis (N > {LIMIT_SEARCH}) ---\n")

        # --- Simulated Annealing ---
        print("--- Testare Simulated Annealing ---")
        start = time.time()
        sol_sa = simulated_annealing(n_disks)
        duration = time.time() - start
        results['Simulated Annealing'] = {'time': duration, 'solution': sol_sa}
        print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_sa is not None else 'NU'}")
        if sol_sa: print(f"Număr mutări: {len(sol_sa)}")
        print("-" * 20 + "\n")

        # --- Recursive Optimal (Standard) ---
        print("--- Testare Recursive Optimal (Standard) ---")
        start = time.time()
        sol_rec = solve_hanoi_recursive(n_disks)
        duration = time.time() - start
        results['Recursive Optimal'] = {'time': duration, 'solution': sol_rec}
        print(f"Timp: {duration:.4f}s. Soluție găsită: DA")
        print(f"Număr mutări: {len(sol_rec)}")
        print("-" * 20 + "\n")

    # Generare raport
    response = output_buffer.getvalue()
    response += "\n=== Concluzie ===\n"

    valid_algos = {}
    for name, res in results.items():
        if res.get('solution') is not None:
            valid_algos[name] = res['time']

    if valid_algos:
        fastest = min(valid_algos, key=valid_algos.get)
        response += f"Cel mai rapid algoritm care a găsit o soluție validă este **{fastest}** ({valid_algos[fastest]:.4f}s).\n"
        
        final_sol = results[fastest]['solution']
        # Limităm afișarea pentru soluții foarte lungi
        if len(final_sol) > 20:
            formatted_sol = format_moves(final_sol[:10]) + "\n... (încă " + str(len(final_sol) - 20) + " mutări) ...\n" + format_moves(final_sol[-10:])
        else:
            formatted_sol = format_moves(final_sol)
            
        response += f"\nSoluția ({fastest}):\n{formatted_sol}"
    else:
        response += "Niciun algoritm nu a găsit o soluție."

    return response
