import io
import time
from contextlib import redirect_stdout

from ai_project.nqueens.algorithms import (
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
    # Suprimăm output-ul funcției pentru a-l integra în răspunsul final
    f = io.StringIO()
    with redirect_stdout(f):
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
    # Suprimăm output-ul funcției pentru a-l integra în răspunsul final
    f = io.StringIO()
    with redirect_stdout(f):
        start_time = time.time()
        # Parametrii pot fi ajustați pentru N mai mare
        solution_mrv = solve_n_queens_mrv(n_size)
        end_time = time.time()
    
    runtime = end_time - start_time
    results["MRV"] = {"time": runtime, "solution": solution_mrv}
    
    print(f"Algoritmul a rulat în {runtime:.4f} secunde.")
    
    return results

def generate_response(n_size, results, limit, user_question):
    """
    Generează un răspuns text la întrebare, bazat pe rezultatele experimentului.
    """
    response = "Răspuns:\n\n"
    response += f"Pentru o tablă de dimensiune {n_size}x{n_size}, am analizat performanța mai multor algoritmi. Iată concluziile:\n\n"

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
    response += (f"- **Simulated Annealing**: A rulat foarte rapid, în {sa_data['time']:.4f} secunde. "
                 f"A găsit o soluție {'optimă (0 conflicte)' if sa_data['conflicts'] == 0 else 'cu ' + str(sa_data['conflicts']) + ' conflicte'}."
                 "\n\n")
    
    mrv_data = results["MRV"]
    response += f"- **MRV**: A rulat în {mrv_data['time']:.4f} secunde. "
    if mrv_data.get("solution"):
        response += "A găsit o soluție optimă (fără conflicte).\n\n"
    else:
        response += "Nu a găsit o soluție.\n\n"

    response += "**Concluzie:**\n"
    if n_size > limit or fastest_algo == "Simulated Annealing":
        response += ("**Simulated Annealing** este cea mai potrivită strategie. Deși nu garantează întotdeauna soluția optimă, "
                     "este extrem de rapid și eficient pentru table de dimensiuni mari, unde algoritmii clasici eșuează. "
                     "În acest caz, a fost cel mai rapid și a găsit o soluție de calitate.")
    else:
        response += (f"**{fastest_algo}** a fost cea mai potrivită strategie, deoarece a găsit o soluție optimă în cel mai scurt timp ({results[fastest_algo]['time']:.4f}s). "
                     "Pentru table mici, unde găsirea unei soluții garantate este importantă și fezabilă, un algoritm de căutare completă ca acesta este ideal.")

    return f"Întrebare: {user_question}\n\n{response}"


