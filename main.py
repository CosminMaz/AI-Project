import sys
import re

from first.nqueens.experiment import run_experiment, generate_response
from second.nash import solve_nash_equilibrium

if __name__ == "__main__":
    """
    Punctul de intrare principal al programului.

    Acesta solicită utilizatorului dimensiunea tablei de șah (N),
    rulează o serie de algoritmi pentru a rezolva problema N-Queens,
    și apoi afișează o comparație și o concluzie despre cea mai bună
    strategie pentru dimensiunea dată.
    """
    user_question = input("Introduceți întrebarea dvs. (ex: Care e cel mai bun algoritm pentru n=8?): ")

    # Verifică dacă întrebarea este despre echilibrul Nash
    if "echilibru nash" in user_question.lower():
        response = solve_nash_equilibrium(user_question)
        print("\n" + "=" * 50 + "\n")
        print(response)
        sys.exit(0)

    # Extrage dimensiunea tablei (N) din întrebare folosind expresii regulate
    match = re.search(r'\b(\d+)\b', user_question)

    try:
        if not match:
            raise ValueError("Nu am putut identifica dimensiunea tablei (N) din întrebare pentru problema N-Queens.")
        n_size = int(match.group(1))
    except ValueError as e:
        print(f"Eroare: {e}", file=sys.stderr)
        sys.exit(1)

    limit = 10  # Limita pentru care se execută algoritmii clasici (DFS, BFS, etc.)

    final_results = run_experiment(n_size, limit)
    final_text = generate_response(n_size, final_results, limit, user_question)

    print("\n" + "=" * 50 + "\n")
    print(final_text)