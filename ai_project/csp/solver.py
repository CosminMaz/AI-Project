import copy
from typing import Dict, List, Any, Optional, Generator, Tuple
from .model import CSP

def revise(csp: CSP, xi: str, xj: str, domains: Dict[str, List[Any]]) -> bool:
    """
    Checks if there is any value in domains[xi] that conflicts with ALL values in domains[xj].
    If so, removes the conflicting value from domains[xi].
    
    Returns: True if domains[xi] was modified.
    """
    revised = False
    
    # We must iterate over a copy because we might remove items
    for x_val in domains[xi][:]:
        satisfiable = False
        
        # Check if there exists ANY value y in xj's domain that satisfies the constraint
        for y_val in domains[xj]:
            # We need to find the constraint object between xi and xj
            # (In an optimized solver, we'd pass the constraint directly, 
            # but here we search neighbors for the generic link)
            is_consistent = True
            for constraint in csp.neighbors[xi]:
                if xj in constraint.variables:
                    # Check this specific pair
                    if not constraint.satisfied({xi: x_val, xj: y_val}):
                        is_consistent = False
                        break
            
            if is_consistent:
                satisfiable = True
                break
        
        # If no value y allows x to exist, delete x
        if not satisfiable:
            domains[xi].remove(x_val)
            revised = True
            
    return revised

def ac3_inference(csp: CSP, queue: List[Tuple[str, str]], domains: Dict[str, List[Any]]) -> bool:
    """
    The AC-3 Algorithm.
    Propagates constraints until consistency is reached or a domain becomes empty.
    
    Args:
        queue: Initial list of arcs (xi, xj) to check.
        domains: The current domain state (will be modified in place).
    """
    while queue:
        (xi, xj) = queue.pop(0)
        
        if revise(csp, xi, xj, domains):
            if not domains[xi]: # Domain became empty -> Failure
                return False
            
            # If xi changed, we need to re-check all neighbors of xi (except xj)
            # because xi's new smaller domain might now restrict them.
            for constraint in csp.neighbors[xi]:
                # Find the neighbor variable
                neighbor = constraint.var1 if constraint.var1 != xi else constraint.var2
                
                if neighbor != xj:
                    queue.append((neighbor, xi))
                    
    return True

def select_unassigned_variable(assignment: Dict[str, Any], csp: CSP, heuristic: str = 'MRV') -> str:
    """
    Selects the next variable to assign.
    
    Strategies:
    - 'first': Pick the first alphabetic unassigned variable.
    - 'MRV' (Minimum Remaining Values): Pick var with fewest legal values left.
    
    CRITICAL: Ties are always broken alphabetically to ensure determinism.
    """
    # Get all variables that are NOT in the current assignment
    unassigned = [v for v in csp.variables if v not in assignment]
    
    # 1. Base Strategy: always sort alphabetically first (deterministic tie-breaking)
    unassigned.sort()
    
    if heuristic == 'MRV':
        # Sort by domain size (ascending), keeping the alphabetical order as secondary sort
        # Python's sort is stable, so equal domain sizes keep alphabetical order.
        unassigned.sort(key=lambda v: len(csp.domains[v]))
        
    return unassigned[0]

def forward_checking(csp: CSP, var: str, value: Any, domains: Dict[str, List[Any]]) -> bool:
    """
    Updates `domains` by removing values inconsistent with `var = value`.
    Returns False if any domain becomes empty (failure), True otherwise.
    """
    # Find neighbors of the current variable
    for constraint in csp.neighbors[var]:
        # Identify the OTHER variable in the constraint
        neighbor = constraint.var1 if constraint.var1 != var else constraint.var2
        
        # If neighbor is already assigned, skip (checked by consistency check earlier)
        # We only prune domains of UNASSIGNED neighbors
        if neighbor not in domains: # This check depends on how we handle domains. 
            # Actually, we should check if neighbor is unassigned in the solver loop.
            # But simpler: if the value is in the domain, try to remove it.
            continue

        # We must iterate over a COPY of the neighbor's domain because we are modifying it
        for n_val in domains[neighbor][:]:
            # Check if this neighbor value is consistent with var=value
            # We treat the neighbor as assigned momentarily to check the constraint
            if not constraint.check(value, n_val) and constraint.var1 == var: 
                # Note: constraint.check logic depends on order. 
                # BinaryConstraint classes need to be agnostic or we reconstruct carefully.
                # Let's rely on the Constraint.satisfied method which is safer:
                pass
            
            # SIMPLER APPROACH for generic constraints:
            # Check if (var=value, neighbor=n_val) violates constraint
            temp_assignment = {var: value, neighbor: n_val}
            if not constraint.satisfied(temp_assignment):
                domains[neighbor].remove(n_val)
        
        if not domains[neighbor]: # Domain became empty!
            return False
            
    return True

# ==========================================
# 2. The Generator Solver
# ==========================================

def solve_step_by_step(
    csp: CSP, 
    assignment: Dict[str, Any] = None, 
    heuristic: str = 'MRV', 
    inference: str = 'FC'
) -> Generator[Tuple[str, Dict, Dict], None, Optional[Dict]]:
    
    if assignment is None:
        assignment = {}

    # 1. Goal Test
    if len(assignment) == len(csp.variables):
        yield ("SOLUTION", assignment, csp.domains)
        return assignment

    # 2. Variable Selection
    var = select_unassigned_variable(assignment, csp, heuristic)

    # 3. Value Ordering
    ordered_values = sorted(csp.domains[var])

    for value in ordered_values:
        
        # 4. Consistency Check
        if csp.is_consistent(var, value, assignment):
            
            # Prepare state
            new_assignment = assignment.copy()
            new_assignment[var] = value
            new_domains = copy.deepcopy(csp.domains)
            
            # We enforce the assignment on the domains immediately
            new_domains[var] = [value] 
            
            inference_success = True
            
            # ==========================================
            # INFERENCE BLOCK (FC vs AC-3)
            # ==========================================
            if inference == 'FC':
                inference_success = forward_checking(csp, var, value, new_domains)
            
            elif inference == 'AC3':
                # Initial Queue for MAC (Maintaining Arc Consistency):
                # Add all arcs (Neighbor -> Var) for unassigned neighbors
                queue = []
                for constraint in csp.neighbors[var]:
                    neighbor = constraint.var1 if constraint.var1 != var else constraint.var2
                    if neighbor not in assignment:
                        queue.append((neighbor, var))
                
                inference_success = ac3_inference(csp, queue, new_domains)
            # ==========================================

            if inference_success:
                yield ("STEP", new_assignment, new_domains)

                # Recursive call with pruned domains
                sub_csp = copy.copy(csp)
                sub_csp.domains = new_domains
                
                result = yield from solve_step_by_step(sub_csp, new_assignment, heuristic, inference)
                
                if result is not None:
                    return result
            
            yield ("BACKTRACK", new_assignment, new_domains)
    
    return None
