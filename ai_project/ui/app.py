from flask import Flask, render_template, request
import sys
from pathlib import Path

# Add the project root to the python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ai_project.nqueens import run_experiment, generate_response
from ai_project.nash import solve_nash_equilibrium
from ai_project.minimax import solve_minimax
from ai_project.csp import solve_csp_problem
from ai_project.graph_coloring.solver import solve_graph_coloring
from ai_project.knights_tour.solver import solve_knights_tour
from ai_project.hanoi.solver import solve_hanoi
from ai_project.ui_v1.app import app as app_v1

from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__, template_folder='templates')
# app.mount('/v1', app_v1)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/v1': app_v1
})


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
        final_results, detailed_logs = run_experiment(n_size, limit)
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
    elif problem_type == 'graph-coloring':
        graph = data.get('graph-coloring-graph', '{}')
        colors = data.get('graph-coloring-colors', '')
        response = solve_graph_coloring(graph, colors)
    elif problem_type == 'knights-tour':
        n_size = int(data.get('knights-tour-size', 5))
        response = solve_knights_tour(n_size)
    elif problem_type == 'hanoi':
        n_disks = int(data.get('hanoi-disks', 3))
        response = solve_hanoi(n_disks)
    else:
        response = "Unknown problem type"

    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)