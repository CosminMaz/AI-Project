import json
import time
import io
from contextlib import redirect_stdout
from .problem import create_coloring_problem
from ai_project.csp.solver import solve_step_by_step
from .algorithms import bfs, dfs, iddfs, simulated_annealing, solve_coloring_mrv, count_conflicts

def solve_graph_coloring(graph_str, colors_str):
    """
    Rezolvă o problemă de colorare a grafului folosind mai mulți algoritmi și compară rezultatele.

    Args:
        graph_str (str): O reprezentare JSON a grafului (listă de adiacență).
        colors_str (str): O listă de culori separate prin virgulă.

    Returns:
        str: Un raport detaliat cu performanța algoritmilor și soluția găsită.
    """
    try:
        graph = json.loads(graph_str)
        colors = [c.strip() for c in colors_str.split(',')]
    except (json.JSONDecodeError, AttributeError):
        return "Format invalid pentru graf sau culori. Graful trebuie să fie un JSON, iar culorile o listă separată de virgule."

    results = {}
    output_buffer = io.StringIO()

    with redirect_stdout(output_buffer):
        print(f"Rezolvare Graph Coloring pentru {len(graph)} noduri și {len(colors)} culori...\n")

        # --- BFS ---
        print("--- Testare BFS ---")
        start = time.time()
        sol_bfs = bfs(graph, colors)
        duration = time.time() - start
        results['BFS'] = {'time': duration, 'solution': sol_bfs}
        print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_bfs else 'NU'}")
        print("-" * 20 + "\n")

        # --- DFS ---
        print("--- Testare DFS ---")
        start = time.time()
        sol_dfs = dfs(graph, colors)
        duration = time.time() - start
        results['DFS'] = {'time': duration, 'solution': sol_dfs}
        print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_dfs else 'NU'}")
        print("-" * 20 + "\n")

        # --- IDDFS ---
        print("--- Testare IDDFS ---")
        start = time.time()
        sol_iddfs = iddfs(graph, colors)
        duration = time.time() - start
        results['IDDFS'] = {'time': duration, 'solution': sol_iddfs}
        print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_iddfs else 'NU'}")
        print("-" * 20 + "\n")

        # --- Simulated Annealing ---
        print("--- Testare Simulated Annealing ---")
        start = time.time()
        sol_sa = simulated_annealing(graph, colors)
        duration = time.time() - start
        conflicts = count_conflicts(graph, sol_sa)
        results['Simulated Annealing'] = {'time': duration, 'solution': sol_sa, 'conflicts': conflicts}
        print(f"Timp: {duration:.4f}s. Conflicte: {conflicts}")
        print("-" * 20 + "\n")

        # --- MRV ---
        print("--- Testare MRV ---")
        start = time.time()
        sol_mrv = solve_coloring_mrv(graph, colors)
        duration = time.time() - start
        results['MRV'] = {'time': duration, 'solution': sol_mrv}
        print(f"Timp: {duration:.4f}s. Soluție găsită: {'DA' if sol_mrv else 'NU'}")
        print("-" * 20 + "\n")

    # Generare raport final
    response = output_buffer.getvalue()
    response += "\n=== Concluzie ===\n"
    
    # Găsește cel mai rapid algoritm valid
    valid_algos = {}
    for name, res in results.items():
        if res['solution']:
            if name == 'Simulated Annealing' and res['conflicts'] > 0:
                continue
            valid_algos[name] = res['time']
    
    if valid_algos:
        fastest = min(valid_algos, key=valid_algos.get)
        response += f"Cel mai rapid algoritm care a găsit o soluție validă este **{fastest}** ({valid_algos[fastest]:.4f}s).\n"
        
        final_sol = results[fastest]['solution']
        formatted_sol = "\n".join([f"{k}: {v}" for k, v in sorted(final_sol.items())])
        response += f"\nSoluția ({fastest}):\n{formatted_sol}"
    else:
        response += "Niciun algoritm nu a găsit o soluție validă completă."

    return response
