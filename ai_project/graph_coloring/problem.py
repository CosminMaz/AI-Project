from ai_project.csp.model import CSP, BinaryConstraint

def create_coloring_problem(graph, colors):
    """
    Creează o problemă de colorare a grafurilor ca o problemă de satisfacere a constrângerilor (CSP).

    Args:
        graph (dict): Un dicționar ce reprezintă un graf neorientat.
                      Cheile sunt nodurile, iar valorile sunt liste de vecini.
                      Exemplu: {'A': ['B', 'C'], 'B': ['A'], 'C': ['A']}
        colors (list): O listă de culori disponibile.
                       Exemplu: ['red', 'green', 'blue']

    Returns:
        CSP: O instanță a clasei CSP care modelează problema de colorare a grafului.
    """
    variables = list(graph.keys())
    domains = {var: list(colors) for var in variables}
    
    constraints = []
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            # Adaugă constrângerea doar o dată pentru fiecare pereche (muchie)
            if node < neighbor:
                constraint = BinaryConstraint(node, neighbor, '!=')
                constraints.append(constraint)
                
    return CSP(variables, domains, constraints)
