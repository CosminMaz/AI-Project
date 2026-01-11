
from .model import CSP, BinaryConstraint
from .solver import solve_step_by_step
import re

def parse_csp_problem(problem_str):
    """
    Parses a CSP problem description string.
    Format: "variables: A, B, C; domains: 1, 2, 3; constraints: A != B, B != C"
    """
    try:
        vars_str = re.search(r'variables:(.*?);', problem_str).group(1).strip()
        doms_str = re.search(r'domains:(.*?);', problem_str).group(1).strip()
        cons_str = re.search(r'constraints:(.*)', problem_str).group(1).strip()

        variables = [v.strip() for v in vars_str.split(',')]
        
        # Check for range vs list
        if '-' in doms_str:
            start, end = map(int, doms_str.split('-'))
            domain = list(range(start, end + 1))
        else:
            domain = [int(d.strip()) for d in doms_str.split(',')]
            
        domains = {var: domain for var in variables}

        constraints = []
        for c_str in cons_str.split(','):
            c_str = c_str.strip()
            match = re.match(r'(\w+)\s*(!=|==|<|>|<=|>=)\s*(\w+)', c_str)
            if match:
                var1, op, var2 = match.groups()
                constraints.append(BinaryConstraint(var1, var2, op))

        return CSP(variables, domains, constraints)
    except Exception as e:
        print(f"Error parsing CSP problem: {e}")
        return None

def solve_csp_problem(problem_str):
    """
    Solves a CSP problem from a string description.
    """
    csp = parse_csp_problem(problem_str)
    if not csp:
        return "Failed to parse CSP problem."

    solver_gen = solve_step_by_step(csp)
    history = list(solver_gen)

    final_event, final_assign, _ = history[-1]

    if final_event == 'SOLUTION':
        return f"Solution found: {final_assign}"
    else:
        return "No solution found."

if __name__ == '__main__':
    problem = "variables: A, B, C; domains: 1-3; constraints: A != B, B != C"
    print(solve_csp_problem(problem))
