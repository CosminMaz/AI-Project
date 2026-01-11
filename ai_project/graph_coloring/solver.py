import json
from .problem import create_coloring_problem
from ai_project.csp.solver import solve_step_by_step

def solve_graph_coloring(graph_str, colors_str):
    """
    Rezolvă o problemă de colorare a grafului.

    Args:
        graph_str (str): O reprezentare JSON a grafului (listă de adiacență).
        colors_str (str): O listă de culori separate prin virgulă.

    Returns:
        str: Un mesaj cu rezultatul.
    """
    try:
        graph = json.loads(graph_str)
        colors = [c.strip() for c in colors_str.split(',')]
    except (json.JSONDecodeError, AttributeError):
        return "Format invalid pentru graf sau culori. Graful trebuie să fie un JSON, iar culorile o listă separată de virgule."

    csp_problem = create_coloring_problem(graph, colors)
    
    solution_generator = solve_step_by_step(csp_problem, inference="ac3")
    
    final_solution = None
    try:
        for status, assignment, _ in solution_generator:
            if status == "SOLUTION":
                final_solution = assignment
                # Ne oprim la prima soluție găsită
                break
    except Exception as e:
        return f"A apărut o eroare în timpul rezolvării: {e}"


    if final_solution:
        # Formatează soluția pentru afișare
        formatted_solution = "\n".join([f"- Nodul {node}: {color}" for node, color in sorted(final_solution.items())])
        return f"Soluție găsită pentru colorarea grafului:\n{formatted_solution}"
    else:
        return "Nu s-a găsit o soluție pentru colorarea grafului cu culorile date."
