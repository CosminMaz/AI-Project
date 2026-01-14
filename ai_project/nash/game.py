"""Representation of normal form games."""

from typing import List, Tuple, Optional


class NormalFormGame:
    """Reprezintă un joc în formă normală cu doi jucători."""
    
    def __init__(
        self,
        payoff_matrix_p1: List[List[float]],
        payoff_matrix_p2: Optional[List[List[float]]] = None,
        player1_strategies: Optional[List[str]] = None,
        player2_strategies: Optional[List[str]] = None
    ):
        """
        Inițializează jocul.
        
        Args:
            payoff_matrix_p1: Matricea de payoff pentru jucătorul 1 (rows x cols)
            payoff_matrix_p2: Matricea de payoff pentru jucătorul 2 (None pentru jocuri simetrice)
            player1_strategies: Numele strategiilor pentru jucătorul 1
            player2_strategies: Numele strategiilor pentru jucătorul 2
        """
        self.payoff_p1 = payoff_matrix_p1
        self.payoff_p2 = payoff_matrix_p2 if payoff_matrix_p2 is not None else payoff_matrix_p1
        
        # Verifică consistența dimensiunilor
        if len(self.payoff_p1) != len(self.payoff_p2):
            raise ValueError("Matricile de payoff trebuie să aibă același număr de linii")
        if any(len(row1) != len(row2) for row1, row2 in zip(self.payoff_p1, self.payoff_p2)):
            raise ValueError("Matricile de payoff trebuie să aibă același număr de coloane")
        
        self.num_rows = len(self.payoff_p1)
        self.num_cols = len(self.payoff_p1[0]) if self.payoff_p1 else 0
        
        # Strategii implicite
        self.player1_strategies = (
            player1_strategies 
            if player1_strategies 
            else [f"Strategia {i+1}" for i in range(self.num_rows)]
        )
        self.player2_strategies = (
            player2_strategies 
            if player2_strategies 
            else [f"Strategia {j+1}" for j in range(self.num_cols)]
        )
    
    def get_payoff(self, row: int, col: int) -> Tuple[float, float]:
        """
        Returnează payoff-urile pentru profilul de strategii (row, col).
        
        Returns:
            (payoff_player1, payoff_player2)
        """
        if not (0 <= row < self.num_rows and 0 <= col < self.num_cols):
            raise IndexError(f"Indici invalizi: ({row}, {col})")
        return self.payoff_p1[row][col], self.payoff_p2[row][col]
    
    def is_zero_sum(self) -> bool:
        """Verifică dacă jocul este zero-sum."""
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if abs(self.payoff_p1[i][j] + self.payoff_p2[i][j]) > 1e-10:
                    return False
        return True
    
    def __repr__(self) -> str:
        return f"NormalFormGame({self.num_rows}x{self.num_cols})"

