def find_pure_nash_equilibrium(matrix, game_name="Joc Generic"):
    """
    Identifică echilibrul Nash pur într-un joc în formă normală (matrice).
    
    :param matrix: O listă de liste, unde fiecare celulă este un tuplu (plata_jucator1, plata_jucator2)
    :return: Lista de echilibre găsite [(rand, coloana, valori)]
    """
    rows = len(matrix)
    cols = len(matrix[0])
    nash_equilibria = []

    print(f"\n--- Analiză pentru: {game_name} ---")

    for r in range(rows):
        for c in range(cols):
            p1_payoff, p2_payoff = matrix[r][c]

            # 1. Verificăm dacă este cea mai bună mișcare pentru Jucătorul 1 (Linii)
            # Comparăm cu toate celelalte opțiuni ale Jucătorului 1 pe aceeași coloană 'c'
            is_best_for_p1 = True
            for other_r in range(rows):
                if matrix[other_r][c][0] > p1_payoff:
                    is_best_for_p1 = False
                    break

            # 2. Verificăm dacă este cea mai bună mișcare pentru Jucătorul 2 (Coloane)
            # Comparăm cu toate celelalte opțiuni ale Jucătorului 2 pe aceeași linie 'r'
            is_best_for_p2 = True
            for other_c in range(cols):
                if matrix[r][other_c][1] > p2_payoff:
                    is_best_for_p2 = False
                    break

            # 3. Dacă e cel mai bine pentru amândoi => Echilibru Nash
            if is_best_for_p1 and is_best_for_p2:
                nash_equilibria.append(((r, c), (p1_payoff, p2_payoff)))

    # Afișare rezultate
    if not nash_equilibria:
        print("Nu există niciun Echilibru Nash Pur.")
    else:
        print(f"S-au găsit {len(nash_equilibria)} Echilibru(e) Nash Pur(e):")
        for pos, payoff in nash_equilibria:
            # Adăugăm +1 la indecși pentru a fi mai ușor de citit (Linia 1 în loc de 0)
            print(f"  -> Strategia: (Linia {pos[0]+1}, Coloana {pos[1]+1}) cu plățile {payoff}")
    
    return nash_equilibria

# ==========================================
# ZONA DE DEFINIRE A JOCURILOR (EXEMPLE)
# Modifică valorile de aici conform matricei tale!
# Format: [ [(P1, P2), (P1, P2)], [(P1, P2), (P1, P2)] ]
# ==========================================

# 1. Dilema Prizonierului (Prisoner's Dilemma)
# De obicei: (Trădare, Trădare) este unicul echilibru Nash, deși (Cooperare, Cooperare) e mai bun global.
prisoners_dilemma = [
    [(-1, -1), (-3, 0)],  # Linia 1: Cooperează
    [(0, -3),  (-2, -2)]  # Linia 2: Trădează
]

# 2. Jocul Lașului (Chicken Game)
# De obicei are două echilibre pure (unul cedează, celălalt merge înainte).
chicken_game = [
    [(0, 0),   (-1, 1)],  # Linia 1: Cedează
    [(1, -1),  (-5, -5)]  # Linia 2: Continuă
]

# 3. Jocul Vânătorii (Stag Hunt)
# Are două echilibre pure: amândoi vânează cerbul sau amândoi vânează iepurele.
stag_hunt = [
    [(3, 3), (0, 2), ],  # Linia 1: Cerb
    [(2, 0), (1, 1)]   # Linia 2: Iepure
]

# 4. Jocul Portarului (The Goalkeeper Game / Matching Pennies)
# Joc de sumă nulă. De obicei NU are echilibru Nash PUR (doar mixt).
goalkeeper_game = [
    [(1, -1), (-1, 1)], # Stânga
    [(-1, 1), (1, -1)]  # Dreapta
]

# --- RULAREA SCRIPTULUI ---
if __name__ == "__main__":
    # AICI POȚI TESTA MATRICEA TA SPECIFICĂ
    # Înlocuiește variabila de mai jos cu definiția matricei tale
    
    find_pure_nash_equilibrium(prisoners_dilemma, "Dilema Prizonierului")
    find_pure_nash_equilibrium(chicken_game, "Jocul Lașului (Chicken)")
    find_pure_nash_equilibrium(stag_hunt, "Vânătoarea (Stag Hunt)")
    find_pure_nash_equilibrium(goalkeeper_game, "Jocul Portarului")