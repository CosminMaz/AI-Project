import copy

class CSP:
    def __init__(self, variables, domains, neighbors, constraint_func):
        """
        :param variables: Lista de variabile (ex: ['A', 'B', 'C'])
        :param domains: Dicționar {variabilă: [valori]}
        :param neighbors: Dicționar {variabilă: [lista_vecini]}
        :param constraint_func: Funcție f(A, a, B, b) care returnează True dacă (A=a) și (B=b) sunt consistente.
        """
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint_func = constraint_func
        self.curr_domains = None  # Se va folosi pentru FC

    def is_consistent(self, var, value, assignment):
        """Verifică dacă valoarea este consistentă cu asignarea curentă."""
        for neighbor in self.neighbors.get(var, []):
            if neighbor in assignment:
                if not self.constraint_func(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        """
        Implementează MRV (Minimum Remaining Values).
        Alege variabila neasignată cu cele mai puține valori rămase în domeniul curent.
        """
        unassigned = [v for v in self.variables if v not in assignment]
        
        # Găsim variabila cu cel mai mic domeniu curent
        best_var = min(unassigned, key=lambda v: len(self.curr_domains[v]))
        return best_var

    def forward_checking(self, var, value, assignment):
        """
        Aplică Forward Checking.
        Elimină valorile inconsistente din domeniile vecinilor neasignați.
        Returnează un dicționar cu valorile eliminate pentru a putea face restore (backtrack).
        """
        pruned = {}  # {neighbor: [removed_values]}
        
        for neighbor in self.neighbors.get(var, []):
            if neighbor not in assignment:
                if neighbor not in pruned:
                    pruned[neighbor] = []
                
                # Iterăm o copie a domeniului pentru a putea modifica originalul
                for n_val in self.curr_domains[neighbor][:]:
                    if not self.constraint_func(var, value, neighbor, n_val):
                        self.curr_domains[neighbor].remove(n_val)
                        pruned[neighbor].append(n_val)
                
                # Dacă un domeniu devine gol, FC a eșuat
                if not self.curr_domains[neighbor]:
                    return False, pruned
                    
        return True, pruned

    def restore_domains(self, pruned):
        """Restaurează valorile eliminate în cazul unui backtrack."""
        for var, values in pruned.items():
            for val in values:
                self.curr_domains[var].append(val)

    def backtrack(self, assignment):
        # 1. Dacă asignarea este completă, am terminat
        if len(assignment) == len(self.variables):
            return assignment

        # 2. Selectare variabilă (MRV)
        var = self.select_unassigned_variable(assignment)

        # 3. Încercăm valorile din domeniul curent (eventual sortate prin LCV - opțional)
        for value in self.curr_domains[var]:
            if self.is_consistent(var, value, assignment):
                # Asignăm
                assignment[var] = value
                
                # Forward Checking
                success, pruned = self.forward_checking(var, value, assignment)
                
                if success:
                    # Apel recursiv
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                
                # Dacă ajungem aici, facem Backtrack
                # 1. Restaurăm domeniile (undo FC)
                self.restore_domains(pruned)
                # 2. Ștergem asignarea
                del assignment[var]
        
        return None

    def solve(self, partial_assignment={}):
        """
        Inițializează procesul de rezolvare pornind de la o asignare parțială.
        """
        self.curr_domains = copy.deepcopy(self.domains)
        assignment = partial_assignment.copy()
        
        # Pas critic: Trebuie să aplicăm FC pentru asignarea parțială inițială
        # pentru a reduce domeniile variabilelor rămase înainte de a începe.
        for var, val in assignment.items():
            if val not in self.domains[var]:
                 print(f"Eroare: Valoarea {val} din asignarea parțială nu e în domeniul variabilei {var}")
                 return None
            self.curr_domains[var] = [val] # Domeniul variabilei asignate devine doar valoarea sa
            
            success, pruned = self.forward_checking(var, val, assignment)
            if not success:
                print("Eroare: Asignarea parțială duce direct la un domeniu vid (inconsistentă).")
                return None

        return self.backtrack(assignment)

# --- ZONA DE CONFIGURARE A PROBLEMEI ---

def exemplu_rulare():
    # 1. Definim Variabilele
    variables = ['A', 'B', 'C', 'D', 'E']

    # 2. Definim Domeniile
    domains = {
        'A': [1, 2, 3],
        'B': [1, 2, 3],
        'C': [1, 2, 3],
        'D': [1, 2, 3],
        'E': [1, 2, 3, 4]
    }

    # 3. Definim Vecinii (Graful constrângerilor)
    # Exemplu: Harta (A e vecin cu B, B cu C etc.)
    neighbors = {
        'A': ['B', 'C'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'E'],
        'D': ['B', 'E'],
        'E': ['C', 'D']
    }

    # 4. Definim Constrângerile
    # Exemplu simplu: Vecinii nu pot avea aceeași valoare (colorarea hărții)
    def constraints(var1, val1, var2, val2):
        return val1 != val2

    # 5. Definim Asignarea Parțială (INPUTUL TĂU)
    partial_assignment = {
        'A': 1
    }

    # --- RULARE ---
    csp = CSP(variables, domains, neighbors, constraints)
    result = csp.solve(partial_assignment)

    print("-" * 30)
    print(f"Asignare Parțială: {partial_assignment}")
    print("-" * 30)
    
    if result:
        print("Soluție găsită (asignarea finală):")
        # Sortăm doar pentru afișare frumoasă
        for k in sorted(result.keys()):
            print(f"{k}: {result[k]}")
    else:
        print("Nu s-a găsit nicio soluție pornind de la această asignare parțială.")

if __name__ == "__main__":
    exemplu_rulare()