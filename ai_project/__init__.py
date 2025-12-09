"""
Core package for the AI-Project exercises.

The package currently exposes:
- N-Queens algorithms and experiment utilities under ``ai_project.nqueens``.
- Nash equilibrium placeholder solver under ``ai_project.nash``.
"""

# Re-export convenience imports for external callers
from ai_project.nash import solve_nash_equilibrium  # noqa: F401
from ai_project.nqueens import (  # noqa: F401
    run_experiment,
    generate_response,
    NQueensProblem,
    bfs,
    dfs,
    iddfs,
    NQueensVisualizer,
    simulated_annealing,
    fast_conflicts,
    solve_n_queens_mrv,
)


