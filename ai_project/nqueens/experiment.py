import io
import time
from contextlib import redirect_stdout
import numpy as np

from .algorithms import (
    NQueensProblem,
    NQueensVisualizer,
    bfs,
    dfs,
    iddfs,
    fast_conflicts,
    simulated_annealing,
    solve_n_queens_mrv,
)


def run_experiment(n_size, limit):
    """
    Rulează toți algoritmii disponibili pentru o dimensiune N dată și compară performanța.
    """
    f = io.StringIO()
    with redirect_stdout(f):
        print(f"Se rulează experimentul pentru N = {n_size}...\n")
        
        results = {}
        visualizer = NQueensVisualizer(symbols=("♛", "·"))

        # --- Algoritmi de căutare clasică (BFS, DFS, IDDFS) ---
        # Acești algoritmi sunt foarte lenți pentru N > 10-12, deci îi rulăm doar pentru N mic.
        classical_algorithms = {
            "DFS": dfs,
            "BFS": bfs,
            "IDDFS": iddfs,
        }

        if n_size <= limit:
            for name, algo_func in classical_algorithms.items():
                print(f"--- Testare {name} ---")
                problem = NQueensProblem(n_size, algo_func)
                start_time = time.time()
                solution = problem.solve()
                end_time = time.time()
                
                runtime = end_time - start_time
                results[name] = {"time": runtime, "solution": solution.queens if solution else None}
                
                if solution:
                    print(f"Soluție găsită în {runtime:.4f} secunde.")
                else:
                    print(f"Nu s-a găsit soluție (sau a durat prea mult). Timp scurs: {runtime:.4f} secunde.")
                print("-" * 20 + "\n")
        else:
            print(f"Algoritmii clasici (DFS, BFS, IDDFS) sunt omiși deoarece N > {limit} și ar dura prea mult.\n")




        # --- Simulated Annealing ---
        print("--- Testare Simulated Annealing ---")
        
        start_time = time.time()
        # Parametrii pot fi ajustați pentru N mai mare
        solution_sa = simulated_annealing(n_size, T=0.01, min_temp=1e-30, decay=0.9995)#T=0.002
        end_time = time.time()
        
        runtime = end_time - start_time
        conflicts = fast_conflicts(solution_sa)
        results["Simulated Annealing"] = {"time": runtime, "solution": solution_sa, "conflicts": conflicts}
        
        print(f"Algoritmul a rulat în {runtime:.4f} secunde.")
        
        if conflicts == 0:
            print("Soluție optimă găsită.")
        else:
            print(f"A fost găsită o soluție cu {conflicts} conflicte.")
        print("-" * 20 + "\n")




        # --- MRV ---
        print("--- Testare MRV ---")
        
        start_time = time.time()
        # Parametrii pot fi ajustați pentru N mai mare
        solution_mrv = solve_n_queens_mrv(n_size)
        end_time = time.time()
        
        runtime = end_time - start_time
        results["MRV"] = {"time": runtime, "solution": solution_mrv}
        
        print(f"Algoritmul a rulat în {runtime:.4f} secunde.")
    
    return results, f.getvalue()

def generate_response(n_size, results, limit, user_question):
    """
    Generează un răspuns text la întrebare, bazat pe rezultatele experimentului.
    """
    response = "Răspuns:\n\n"
    response += f"Pentru o tablă de dimensiune {n_size}x{n_size}, am analizat performanța mai multor algoritmi. Iată concluziile:\n\n"

    # Identificăm cel mai rapid algoritm care a găsit o soluție validă (fără conflicte)
    valid_results = {}
    for name, data in results.items():
        # Verificăm dacă algoritmul a găsit o soluție
        if data.get('solution') is not None:
            # Pentru SA, verificăm explicit numărul de conflicte
            if name == "Simulated Annealing":
                if data.get('conflicts', 0) == 0:
                    valid_results[name] = data['time']
            # Pentru ceilalți algoritmi (MRV, DFS, etc.), presupunem că dacă returnează o soluție, e validă
            else:
                valid_results[name] = data['time']

    if valid_results:
        fastest_algo = min(valid_results, key=valid_results.get)
    else:
        # Dacă nimeni nu a găsit soluție validă, luăm cel mai rapid indiferent de rezultat
        fastest_algo = min(results, key=lambda k: results[k]['time'])


    if n_size <= limit:
        response += ("La această dimensiune, algoritmii de căutare clasică precum DFS, BFS și IDDFS sunt capabili "
                     "să găsească o soluție garantat optimă (fără conflicte). Totuși, timpii lor de execuție pot varia.\n\n")
        for name, data in results.items():
            if name in ["DFS", "BFS", "IDDFS"]:
                 response += f"- **{name}**: A găsit o soluție în {data['time']:.4f} secunde.\n"
    else:
        response += ("La această dimensiune, algoritmii de căutare clasică (DFS, BFS, IDDFS) devin impracticabili din cauza "
                     "complexității exponențiale. Ei ar consuma o cantitate foarte mare de timp și memorie.\n\n")

    sa_data = results["Simulated Annealing"]
    response += (f"- **Simulated Annealing**: A rulat în {sa_data['time']:.4f} secunde. "
                 f"A găsit o soluție {'optimă (0 conflicte)' if sa_data['conflicts'] == 0 else 'cu ' + str(sa_data['conflicts']) + ' conflicte'}."
                 "\n\n")
    
    mrv_data = results["MRV"]
    response += f"- **MRV**: A rulat în {mrv_data['time']:.4f} secunde. "
    if mrv_data.get("solution"):
        response += "A găsit o soluție optimă (fără conflicte).\n\n"
    else:
        response += "Nu a găsit o soluție.\n\n"

    response += "**Concluzie:**\n"
    
    response += f"**{fastest_algo}** a fost cea mai potrivită strategie în acest caz, deoarece a găsit o soluție optimă în cel mai scurt timp ({results[fastest_algo]['time']:.4f}s). "

    if fastest_algo == "Simulated Annealing":
        response += "Este extrem de eficient pentru probleme de optimizare pe spații mari de stări, deși are o componentă probabilistică."
    elif fastest_algo == "MRV":
        response += "Heuristica MRV (Minimum Remaining Values) a redus drastic spațiul de căutare, permițând găsirea rapidă a soluției fără a explora toate posibilitățile inutile."
    elif fastest_algo in ["DFS", "BFS", "IDDFS"]:
        response += "Pentru table mici, algoritmii de căutare completă sunt ideali deoarece garantează găsirea soluției."

    # Afișăm soluția găsită de cel mai bun algoritm
    best_solution = results[fastest_algo].get('solution')
    if best_solution is not None:
        response += "\n\n**Soluția găsită:(Regina i se afla pe coloana v[i] in matrice)**\n"
        # Convertim soluția într-un format lizibil (listă de poziții)
        if isinstance(best_solution, np.ndarray):
             response += str(best_solution.tolist())
        else:
             response += str(best_solution)

    return f"Întrebare: {user_question}\n\n{response}"
