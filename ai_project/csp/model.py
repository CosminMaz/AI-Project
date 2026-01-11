import random
import copy
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple

# ==========================================
# 1. Constraint Classes
# ==========================================

class Constraint(ABC):
    """Abstract base class for all constraints."""
    def __init__(self, variables: List[str]):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[str, Any]) -> bool:
        """Returns True if the constraint is satisfied given the assignment."""
        pass

    @abstractmethod
    def __str__(self):
        pass

class BinaryConstraint(Constraint):
    """A constraint between exactly two variables."""
    def __init__(self, var1: str, var2: str, op: str):
        super().__init__([var1, var2])
        self.var1 = var1
        self.var2 = var2
        self.op = op

    def satisfied(self, assignment: Dict[str, Any]) -> bool:
        # If either variable is not assigned yet, the constraint cannot be violated
        if self.var1 not in assignment or self.var2 not in assignment:
            return True
        return self.check(assignment[self.var1], assignment[self.var2])

    def check(self, val1, val2) -> bool:
        """Actual logic comparing two values."""
        if self.op == '!=':
            return val1 != val2
        if self.op == '==':
            return val1 == val2
        if self.op == '<':
            return val1 < val2
        if self.op == '>':
            return val1 > val2
        if self.op == '<=':
            return val1 <= val2
        if self.op == '>=':
            return val1 >= val2
        return False
    
    def __str__(self):
        return f"{self.var1} {self.op} {self.var2}"

# ==========================================
# 2. The CSP Model
# ==========================================

class CSP:
    """Represents the Constraint Satisfaction Problem state."""
    def __init__(self, variables: List[str], domains: Dict[str, List[Any]], constraints: List[Constraint] = None):
        self.variables = variables
        self.domains = domains
        self.constraints: List[Constraint] = constraints if constraints is not None else []
        
        # Adjacency list: Map variable -> List of constraints it is involved in
        # Crucial for efficient Forward Checking and AC-3
        self.neighbors: Dict[str, List[Constraint]] = {v: [] for v in variables}
        if constraints:
            for constraint in self.constraints:
                for var in constraint.variables:
                    if var in self.neighbors:
                        self.neighbors[var].append(constraint)


    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)
        for var in constraint.variables:
            if var in self.neighbors:
                self.neighbors[var].append(constraint)

    def is_consistent(self, var: str, value: Any, assignment: Dict[str, Any]) -> bool:
        """
        Checks if assigning `value` to `var` conflicts with any CURRENTLY
        assigned variables in `assignment`.
        """
        # We simulate the assignment temporarily
        # (Optimization: In a tight loop, we might pass values directly, 
        # but this is safer for general logic)
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        
        for constraint in self.neighbors[var]:
            # If the neighbor in this constraint is not assigned, satisfied() returns True.
            # If it is assigned, it checks the logic.
            if not constraint.satisfied(temp_assignment):
                return False
        return True

    def __str__(self):
        s = "--- CSP Model ---\n"
        s += f"Variables: {', '.join(self.variables)}\n"
        s += "Domains:\n"
        for v in self.variables:
            s += f"  {v}: {self.domains[v]}\n"
        s += "Constraints:\n"
        for c in self.constraints:
            s += f"  {c}\n"
        return s

# ==========================================
# 3. Random CSP Generator
# ==========================================

class CSPGenerator:
    # Pre-defined vocabularies for "Word" domains
    COLORS = ['Red', 'Green', 'Blue', 'Yellow', 'Cyan', 'Magenta', 'White', 'Black']
    FRUITS = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape']
    
    @staticmethod
    def generate(
        num_vars: int = 4, 
        domain_type: str = 'numbers', # 'numbers' or 'colors' or 'fruits'
        min_domain_size: int = 2,
        max_domain_size: int = 4,
        topology: str = 'random_connected', 
        density: float = 0.4
    ) -> CSP:
        
        # 1. Create Variables
        variables = [chr(65 + i) for i in range(num_vars)]
        
        # 2. Create Diverse Domains
        domains = {}
        for var in variables:
            # Pick a random size for this specific variable
            size = random.randint(min_domain_size, max_domain_size)
            
            if domain_type == 'numbers':
                # Random subset of 1..10 to make it interesting
                # (e.g., A=[1,5,9], B=[2,3])
                vals = sorted(random.sample(range(1, 10), size))
                domains[var] = vals
            elif domain_type == 'colors':
                domains[var] = sorted(random.sample(CSPGenerator.COLORS, size))
            elif domain_type == 'fruits':
                domains[var] = sorted(random.sample(CSPGenerator.FRUITS, size))
        
        model = CSP(variables, domains)
        
        # 3. Build Constraints
        # CRITICAL: If using words, only use NotEqual to avoid confusion.
        allow_inequality = (domain_type == 'numbers')
        
        if topology == 'chain':
            CSPGenerator._build_chain(model, variables, allow_inequality)
        elif topology == 'cycle':
            CSPGenerator._build_cycle(model, variables, allow_inequality)
        elif topology == 'complete':
            CSPGenerator._build_complete(model, variables, allow_inequality)
        else:
            CSPGenerator._build_random_connected(model, variables, density, allow_inequality)
            
        return model

    # --- Updated Helper to respect data types ---

    @staticmethod
    def _get_random_binary_constraint(var1, var2, allow_inequality=True):
        if allow_inequality:
            op = random.choice(['!=', '<', '>'])
        else:
            op = '!='
            
        return BinaryConstraint(var1, var2, op)

    # Update the build methods to accept the 'allow_inequality' flag
    # and pass it to _get_random_binary_constraint
    @staticmethod
    def _build_chain(model, vars, allow_ineq):
        for i in range(len(vars) - 1):
            c = CSPGenerator._get_random_binary_constraint(vars[i], vars[i+1], allow_ineq)
            model.add_constraint(c)

    @staticmethod
    def _build_cycle(model, vars, allow_ineq):
        CSPGenerator._build_chain(model, vars, allow_ineq)
        c = CSPGenerator._get_random_binary_constraint(vars[-1], vars[0], allow_ineq)
        model.add_constraint(c)

    @staticmethod
    def _build_complete(model, vars, allow_ineq):
        for i in range(len(vars)):
            for j in range(i + 1, len(vars)):
                c = CSPGenerator._get_random_binary_constraint(vars[i], vars[j], allow_ineq)
                model.add_constraint(c)

    @staticmethod
    def _build_random_connected(model, vars, density, allow_ineq):
        shuffled = vars[:]
        random.shuffle(shuffled)
        existing_edges = set()

        # Spanning Tree
        for i in range(len(shuffled) - 1):
            v1, v2 = shuffled[i], shuffled[i+1]
            c = CSPGenerator._get_random_binary_constraint(v1, v2, allow_ineq)
            model.add_constraint(c)
            existing_edges.add(tuple(sorted((v1, v2))))

        # Random Edges
        n = len(vars)
        max_edges = (n * (n - 1)) // 2
        target_edges = int(max_edges * density)
        target_edges = max(target_edges, n - 1)

        while len(model.constraints) < target_edges:
            v1, v2 = random.sample(vars, 2)
            edge_key = tuple(sorted((v1, v2)))
            if edge_key not in existing_edges:
                c = CSPGenerator._get_random_binary_constraint(v1, v2, allow_ineq)
                model.add_constraint(c)
                existing_edges.add(edge_key)

                
# --- Quick Test ---
if __name__ == "__main__":
    # Test generation
    csp = CSPGenerator.generate(num_vars=4, min_domain_size=3, topology='chain')
    print(csp)
