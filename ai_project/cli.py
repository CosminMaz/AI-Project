import re
import sys

from ai_project.nash import solve_nash_equilibrium
from ai_project.nqueens import generate_response, run_experiment


def main():
    """
    Entry point for the console application.

    It parses the user question, chooses the appropriate solver (N-Queens or
    Nash equilibrium), runs the computation, and prints a formatted answer.
    """
    user_question = input(
        "Introduceți întrebarea dvs. (ex: Care e cel mai bun algoritm pentru n=8?): "
    )

    # Route Nash equilibrium questions directly to the corresponding solver.
    if "echilibru nash" in user_question.lower():
        response = solve_nash_equilibrium(user_question)
        print("\n" + "=" * 50 + "\n")
        print(response)
        sys.exit(0)

    # Extract the board size (N) from the question using regex.
    match = re.search(r"\b(\d+)\b", user_question)

    try:
        if not match:
            raise ValueError(
                "Nu am putut identifica dimensiunea tablei (N) din întrebare pentru problema N-Queens."
            )
        n_size = int(match.group(1))
    except ValueError as exc:
        print(f"Eroare: {exc}", file=sys.stderr)
        sys.exit(1)

    # Limit for executing classical algorithms (DFS, BFS, etc.)
    limit = 10

    final_results = run_experiment(n_size, limit)
    final_text = generate_response(n_size, final_results, limit, user_question)

    print("\n" + "=" * 50 + "\n")
    print(final_text)


if __name__ == "__main__":
    main()


