"""Parser for extracting game matrices from user input text."""

import re
from typing import List, Tuple, Optional


def parse_matrix_from_text(text: str) -> Optional[List[List[float]]]:
    """
    Extrage o matrice din text, acceptând diverse formate.
    
    Caută pattern-uri precum:
    - Matrici între paranteze: [[1,2],[3,4]]
    - Matrici cu linii separate prin newline sau virgulă
    - Numere separate prin spații, virgule sau tab-uri
    """
    # Pattern pentru matrice între paranteze pătrate
    bracket_pattern = r'\[\[([^\]]+)\]\]'
    bracket_match = re.search(bracket_pattern, text)
    
    if bracket_match:
        try:
            # Încearcă să evalueze direct dacă e format Python valid
            matrix_str = bracket_match.group(0)
            matrix = eval(matrix_str)  # Safe pentru input controlat
            if isinstance(matrix, list) and all(isinstance(row, list) for row in matrix):
                return [[float(x) for x in row] for row in matrix]
        except:
            pass
    
    # Pattern pentru linii de numere separate prin spații/virgule
    # Caută secțiuni care arată ca matrici (mai multe linii cu numere)
    lines = text.split('\n')
    matrix_lines = []
    
    for line in lines:
        # Elimină spații și caută numere
        numbers = re.findall(r'-?\d+\.?\d*', line)
        if len(numbers) >= 2:  # Cel puțin 2 numere pe linie
            try:
                row = [float(n) for n in numbers]
                matrix_lines.append(row)
            except ValueError:
                continue
    
    if len(matrix_lines) >= 2 and all(len(row) == len(matrix_lines[0]) for row in matrix_lines):
        return matrix_lines
    
    # Pattern pentru matrice formatată ca tabel (spații/tab-uri)
    # Caută blocuri consecutive de linii cu numere
    number_pattern = r'-?\d+\.?\d*'
    all_numbers = re.findall(number_pattern, text)
    
    if len(all_numbers) >= 4:  # Cel puțin o matrice 2x2
        try:
            numbers = [float(n) for n in all_numbers]
            # Încearcă să ghicească dimensiunea (pătrat perfect sau 2xN)
            n = len(numbers)
            # Pentru matrice pătrată
            sqrt_n = int(n ** 0.5)
            if sqrt_n * sqrt_n == n:
                matrix = [numbers[i:i+sqrt_n] for i in range(0, n, sqrt_n)]
                return matrix
            # Pentru matrice 2xN sau Nx2
            if n % 2 == 0:
                rows = n // 2
                matrix = [numbers[i:i+2] for i in range(0, n, 2)]
                if len(matrix) == rows:
                    return matrix
        except ValueError:
            pass
    
    return None


def parse_payoff_matrices(text: str) -> Optional[Tuple[List[List[float]], List[List[float]]]]:
    """
    Extrage două matrici de payoff pentru jocuri cu doi jucători.
    
    Returnează (payoff_matrix_player1, payoff_matrix_player2) sau None.
    """
    # Caută două matrici consecutive sau separate explicit

    # Pattern pentru două blocuri de matrici
    # Format: matrice1 apoi matrice2 sau (a1,b1), (a2,b2) etc.
    
    # Format (a,b) pentru payoff-uri pereche
    pair_pattern = r'\((-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\)'
    pairs = re.findall(pair_pattern, text)
    
    if pairs:
        try:
            payoffs = [(float(a), float(b)) for a, b in pairs]
            # Organizează în matrici dacă e posibil
            n = len(payoffs)
            sqrt_n = int(n ** 0.5)
            if sqrt_n * sqrt_n == n:
                matrix1 = [[payoffs[i*sqrt_n + j][0] for j in range(sqrt_n)] 
                           for i in range(sqrt_n)]
                matrix2 = [[payoffs[i*sqrt_n + j][1] for j in range(sqrt_n)] 
                           for i in range(sqrt_n)]
                return matrix1, matrix2
        except ValueError:
            pass
    
    # Caută două matrici separate
    # Pattern pentru "Player 1:" sau "Jucător 1:" urmat de matrice
    player_patterns = [
        r'(?:player\s*1|jucător\s*1|p1)[:\s]*\[?\[?([^\]]+)\]?\]?',
        r'(?:player\s*2|jucător\s*2|p2)[:\s]*\[?\[?([^\]]+)\]?\]?',
    ]
    
    # Alternativ: caută două blocuri de numere consecutive
    all_numbers = re.findall(r'-?\d+\.?\d*', text)
    if len(all_numbers) >= 8:  # Cel puțin două matrici 2x2
        try:
            numbers = [float(n) for n in all_numbers]
            n = len(numbers) // 2
            # Presupunem că prima jumătate e pentru player 1, a doua pentru player 2
            sqrt_n = int(n ** 0.5)
            if sqrt_n * sqrt_n == n:
                matrix1 = [numbers[i:i+sqrt_n] for i in range(0, n, sqrt_n)]
                matrix2 = [numbers[i:i+sqrt_n] for i in range(n, 2*n, sqrt_n)]
                return matrix1, matrix2
        except ValueError:
            pass
    
    # Dacă nu găsim două matrici, încercăm să extragem o singură matrice
    # și să o folosim pentru ambele (zero-sum game sau simetrie)
    single_matrix = parse_matrix_from_text(text)
    if single_matrix:
        # Pentru jocuri simetrice sau zero-sum, folosim aceeași matrice
        return single_matrix, single_matrix
    
    return None


def extract_matrix_dimensions(text: str) -> Optional[Tuple[int, int]]:
    """Extrage dimensiunile matricei menționate în text."""
    # Pattern pentru "n x m" sau "n×m" sau "n*m"
    dim_pattern = r'(\d+)\s*[x×*]\s*(\d+)'
    match = re.search(dim_pattern, text, re.IGNORECASE)
    if match:
        return int(match.group(1)), int(match.group(2))
    
    # Pattern pentru "matrice nxn" sau "n by n"
    square_pattern = r'(\d+)\s*x\s*\1|(\d+)\s*×\s*\2|(\d+)\s*by\s*\3'
    match = re.search(square_pattern, text, re.IGNORECASE)
    if match:
        n = int(match.group(1) or match.group(2) or match.group(3))
        return n, n
    
    return None

