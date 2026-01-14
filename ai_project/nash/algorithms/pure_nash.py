"""Algorithm for finding pure Nash equilibria in normal form games."""

from typing import List, Tuple
from ai_project.nash.game import NormalFormGame

EPSILON = 1e-9

def find_pure_nash_equilibria(game: NormalFormGame) -> List[Tuple[int, int]]:
    """
    Găsește toate echilibrele Nash pure într-un joc în formă normală.
    
    Un echilibru Nash pur este un profil de strategii (i, j) astfel încât:
    - Jucătorul 1 nu poate îmbunătăți payoff-ul schimbând strategia (i este răspunsul său optim la j)
    - Jucătorul 2 nu poate îmbunătăți payoff-ul schimbând strategia (j este răspunsul său optim la i)
    
    Args:
        game: Jocul în formă normală
        
    Returns:
        Lista de tupluri (row, col) reprezentând echilibrele Nash pure
    """
    equilibria = []
    
    # Pentru fiecare profil de strategii (i, j)
    for i in range(game.num_rows):
        for j in range(game.num_cols):
            payoff_p1, payoff_p2 = game.get_payoff(i, j)
            
            # Verifică dacă i este răspunsul optim al jucătorului 1 la strategia j a jucătorului 2
            is_best_response_p1 = True
            for k in range(game.num_rows):
                p1_payoff_at_k = game.payoff_p1[k][j]
                # Dacă există o strategie k care oferă un payoff strict mai mare (cu toleranță)
                if p1_payoff_at_k > payoff_p1 + EPSILON:
                    is_best_response_p1 = False
                    break
            
            # Verifică dacă j este răspunsul optim al jucătorului 2 la strategia i a jucătorului 1
            is_best_response_p2 = True
            for k in range(game.num_cols):
                p2_payoff_at_k = game.payoff_p2[i][k]
                # Dacă există o strategie k care oferă un payoff strict mai mare (cu toleranță)
                if p2_payoff_at_k > payoff_p2 + EPSILON:
                    is_best_response_p2 = False
                    break
            
            # Dacă ambele condiții sunt îndeplinite, avem un echilibru Nash
            if is_best_response_p1 and is_best_response_p2:
                equilibria.append((i, j))
    
    return equilibria


def find_best_responses(game: NormalFormGame) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Găsește răspunsurile optime pentru fiecare jucător.
    
    Returns:
        (best_responses_p1, best_responses_p2) unde:
        - best_responses_p1[j] = lista de strategii optime ale jucătorului 1 când jucătorul 2 joacă strategia j
        - best_responses_p2[i] = lista de strategii optime ale jucătorului 2 când jucătorul 1 joacă strategia i
    """
    best_responses_p1 = []
    for j in range(game.num_cols):
        best_payoff = max(game.payoff_p1[i][j] for i in range(game.num_rows))
        best_strategies = [
            i for i in range(game.num_rows) 
            if abs(game.payoff_p1[i][j] - best_payoff) < EPSILON
        ]
        best_responses_p1.append(best_strategies)
    
    best_responses_p2 = []
    for i in range(game.num_rows):
        best_payoff = max(game.payoff_p2[i][j] for j in range(game.num_cols))
        best_strategies = [
            j for j in range(game.num_cols) 
            if abs(game.payoff_p2[i][j] - best_payoff) < EPSILON
        ]
        best_responses_p2.append(best_strategies)
    
    return best_responses_p1, best_responses_p2