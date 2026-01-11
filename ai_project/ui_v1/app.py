from flask import Flask, render_template, request
import sys
from pathlib import Path

# Add the project root to the python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ai_project.nqueens import run_experiment, generate_response
from ai_project.nash import solve_nash_equilibrium
from ai_project.minimax import solve_minimax
from ai_project.csp import solve_csp_problem

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem_type = data.get('problem-type')

    if problem_type == 'nqueens':
        n_size = int(data.get('n-size', 8))
        limit = 8
        final_results = run_experiment(n_size, limit)
        response = generate_response(n_size, final_results, limit, f"N-Queens for N={n_size}")
    elif problem_type == 'nash':
        matrix = data.get('nash-matrix', '')
        response = solve_nash_equilibrium(matrix)
    elif problem_type == 'minimax':
        tree = data.get('minimax-tree', '')
        response = solve_minimax(tree)
    elif problem_type == 'csp':
        problem = data.get('csp-problem', '')
        response = solve_csp_problem(problem)
    else:
        response = "Unknown problem type"

    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)
