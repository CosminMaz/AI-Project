"""Solver for Nash equilibrium analysis."""

from ai_project.nash.parser import parse_payoff_matrices, parse_matrix_from_text
from ai_project.nash.game import NormalFormGame
from ai_project.nash.algorithms import find_pure_nash_equilibria


def solve_nash_equilibrium(user_question: str) -> str:
    """
    Analizează întrebarea despre echilibrul Nash și returnează un răspuns.
    
    Args:
        user_question: Întrebarea utilizatorului care poate conține matricea jocului
        
    Returns:
        Răspuns formatat despre echilibrele Nash găsite
    """
    response = f"Întrebare: {user_question}\n\n"
    response += "Răspuns:\n\n"
    
    # Încearcă să extragă matricile de payoff din întrebare
    payoff_matrices = parse_payoff_matrices(user_question)
    
    # Dacă nu găsim matricile în text, solicităm input interactiv
    if payoff_matrices is None:
        print("\nNu am putut identifica matricea jocului în întrebare.")
        print("Vă rugăm să introduceți matricea de payoff.\n")
        
        # Solicităm matricea pentru jucătorul 1
        print("Introduceți matricea de payoff pentru Jucătorul 1")
        print("(format: fiecare linie pe o linie nouă, numere separate prin spații)")
        print("Exemplu pentru matrice 2x2:")
        print("  3 1")
        print("  0 2")
        
        matrix1_lines = []
        while True:
            line = input("Linie (gol pentru a termina): ").strip()
            if not line:
                break
            try:
                row = [float(x) for x in line.split()]
                matrix1_lines.append(row)
            except ValueError:
                print("Linie invalidă, încercați din nou.")
        
        if not matrix1_lines:
            return response + "Eroare: Nu a fost introdusă nicio matrice validă."
        
        # Verifică dacă toate liniile au aceeași lungime
        num_cols = len(matrix1_lines[0])
        if not all(len(row) == num_cols for row in matrix1_lines):
            return response + "Eroare: Toate liniile trebuie să aibă același număr de elemente."
        
        # Solicităm matricea pentru jucătorul 2 (sau folosim aceeași pentru jocuri simetrice)
        print("\nIntroduceți matricea de payoff pentru Jucătorul 2")
        print("(sau apăsați Enter pentru a folosi aceeași matrice - joc simetric)")
        
        matrix2_lines = []
        line = input("Linie (gol pentru a termina sau pentru joc simetric): ").strip()
        if line:
            matrix2_lines.append([float(x) for x in line.split()])
            while True:
                line = input("Linie (gol pentru a termina): ").strip()
                if not line:
                    break
                try:
                    row = [float(x) for x in line.split()]
                    matrix2_lines.append(row)
                except ValueError:
                    print("Linie invalidă, încercați din nou.")
            
            if len(matrix2_lines) != len(matrix1_lines) or \
               not all(len(row) == num_cols for row in matrix2_lines):
                return response + "Eroare: Matricea jucătorului 2 trebuie să aibă aceleași dimensiuni."
            payoff_matrices = (matrix1_lines, matrix2_lines)
        else:
            # Joc simetric - folosește aceeași matrice
            payoff_matrices = (matrix1_lines, matrix1_lines)
    
    try:
        # Creează obiectul joc
        game = NormalFormGame(
            payoff_matrix_p1=payoff_matrices[0],
            payoff_matrix_p2=payoff_matrices[1]
        )
        
        # Găsește echilibrele Nash pure
        equilibria = find_pure_nash_equilibria(game)
        
        # Formatează răspunsul
        response += f"Am analizat jocul în formă normală ({game.num_rows}x{game.num_cols}).\n\n"
        
        if game.is_zero_sum():
            response += "Jocul este zero-sum.\n\n"
        
        if equilibria:
            response += f"**Există {len(equilibria)} echilibru/echilibre Nash pur(e):**\n\n"
            for idx, (i, j) in enumerate(equilibria, 1):
                payoff_p1, payoff_p2 = game.get_payoff(i, j)
                response += (
                    f"{idx}. ({game.player1_strategies[i]}, {game.player2_strategies[j]})\n"
                    f"   Payoff-uri: Jucătorul 1 = {payoff_p1}, Jucătorul 2 = {payoff_p2}\n\n"
                )
        else:
            response += "**Nu există echilibru Nash pur.**\n\n"
            response += "În acest caz, ar trebui să căutați echilibre Nash în strategii mixte.\n"
        
        return response
        
    except Exception as e:
        return response + f"Eroare la procesarea jocului: {str(e)}\n"


