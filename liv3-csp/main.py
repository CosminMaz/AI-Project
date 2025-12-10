import random
import sys
from typing import List, Tuple, Dict, Any

# Import our custom modules
from model import CSPGenerator, CSP
from solver import solve_step_by_step

# ==========================================
# 1. Helper Functions for User Input
# ==========================================

def get_int_input(prompt: str, default: int, min_val: int = 1) -> int:
    """Safely gets an integer input with a default fallback."""
    try:
        user_in = input(f"{prompt} [default: {default}]: ").strip()
        if not user_in:
            return default
        val = int(user_in)
        if val < min_val:
            print(f"Value must be at least {min_val}.")
            return get_int_input(prompt, default, min_val)
        return val
    except ValueError:
        print("Invalid number.")
        return get_int_input(prompt, default, min_val)

def get_choice_input(prompt: str, choices: List[str], default: str) -> str:
    """Safely gets a string input from a list of valid choices."""
    c_str = "/".join(choices)
    user_in = input(f"{prompt} ({c_str}) [default: {default}]: ").strip().upper()
    if not user_in:
        return default
    if user_in in choices:
        return user_in
    print(f"Invalid choice. Please choose from {choices}.")
    return get_choice_input(prompt, choices, default)

def get_value_input(prompt: str, data_type: str) -> Any:
    """
    Reads input and converts it to int if data_type is 'numbers',
    otherwise keeps it as a title-cased string (e.g., 'red' -> 'Red').
    """
    user_in = input(f"{prompt}: ").strip()
    
    if data_type == 'numbers':
        try:
            return int(user_in)
        except ValueError:
            print("Please enter a valid number.")
            return get_value_input(prompt, data_type)
    else:
        # For colors/fruits, handle capitalization automatically for better UX
        return user_in.title()

def print_separator():
    print("-" * 60)

# ==========================================
# 2. Main Game Loop
# ==========================================

def main():
    print_separator()
    print("CSP GENERATOR")
    print_separator()

    # --- Configuration Phase ---
    num_vars = get_int_input("Number of Variables", 4)
    
    # New: Ask for Data Type
    domain_type = get_choice_input(
        "Domain Type", 
        ['NUMBERS', 'COLORS', 'FRUITS'], 
        'NUMBERS'
    ).lower()

    # New: Ask for Domain Size Range
    min_size = get_int_input("Min Domain Size", 2)
    max_size = get_int_input("Max Domain Size", 5)
    if max_size < min_size:
        max_size = min_size
        print(f"Adjusted Max Domain Size to {max_size}")
    
    topology = get_choice_input(
        "Graph Topology", 
        ['CHAIN', 'CYCLE', 'COMPLETE', 'RANDOM'], 
        'RANDOM'
    )
    
    heuristic = get_choice_input(
        "Variable Heuristic", 
        ['MRV', 'NONE'], 
        'MRV'
    )
    # Map NONE to the code's expectation (which uses 'first' or just None check)
    heuristic_code = 'MRV' if heuristic == 'MRV' else 'first'

    inference = get_choice_input(
        "Inference Strategy", 
        ['FC', 'AC3', 'NONE'], 
        'FC'
    )
    inference_code = inference if inference != 'NONE' else None

    # --- Generation Phase ---
    print("\n... Generating CSP Model ...")
    
    # Map friendly names to internal generator names
    topo_map = {
        'CHAIN': 'chain', 
        'CYCLE': 'cycle', 
        'COMPLETE': 'complete', 
        'RANDOM': 'random_connected'
    }
    
    # Call the updated generator with all new parameters
    csp = CSPGenerator.generate(
        num_vars=num_vars, 
        domain_type=domain_type,
        min_domain_size=min_size,
        max_domain_size=max_size,
        topology=topo_map[topology]
    )
    
    print("\nProblem Generated:")
    print(csp)

    # --- Simulation Phase (Pre-calculation) ---
    print("... Running Solver internally to generate timeline ...")
    
    # We store the full history of the solver: [(event, assignment, domains), ...]
    history: List[Tuple[str, Dict, Dict]] = []
    
    # Create the generator
    solver_gen = solve_step_by_step(csp, heuristic=heuristic_code, inference=inference_code)
    
    # Unroll the generator completely
    for step in solver_gen:
        history.append(step)

    # Filter out only interesting steps (We don't want to quiz on the final solution immediately)
    if len(history) < 2:
        print("\n[!] The problem was solved (or failed) too quickly (0 or 1 step).")
        print("    Try increasing variables or domain size.")
        return

    # --- Quiz Phase ---
    
    # We want to pick a random step, but favor earlier steps to keep it interesting.
    # Uniform random (randint) is boring because it often picks steps where 
    # the puzzle is 90% done.
    
    max_index = len(history) - 2
    
    # approach: Use a "Triangular" distribution
    # low=0, high=max_index, mode=0
    # The 'mode' is the peak of the probability, so setting it to 0
    # makes the very first steps the most likely to be picked.
    if max_index > 0:
        weighted_index = int(random.triangular(0, max_index, 0))
        quiz_index = weighted_index
    else:
        # Fallback if history is tiny
        quiz_index = 0
    
    current_state = history[quiz_index]
    next_state = history[quiz_index + 1]
    
    event_type, current_assignment, current_domains = current_state
    
    # -- Safety Check: Ensure we don't ask about a completed state --
    # If by chance we picked a state where all variables are already assigned
    # (rare, but possible if the solver yields an extra step), walk back one step.
    if len(current_assignment) == len(csp.variables) and quiz_index > 0:
        quiz_index -= 1
        current_state = history[quiz_index]
        next_state = history[quiz_index + 1]
        event_type, current_assignment, current_domains = current_state

    print_separator()
    print(f"🛑 STOPPING SOLVER AT STEP {quiz_index + 1} (of {len(history)}) 🛑")
    print_separator()
    
    # ... Rest of the print logic remains the same ...    
    print(f"Current Event: {event_type}")
    print(f"Current Partial Assignment: {current_assignment}")
    if inference_code:
        print(f"Current Pruned Domains ({inference}):")
        for k, v in current_domains.items():
            print(f"  {k}: {v}")
    else:
        # Show static domains if no inference
        print("Current Domains (Static):")
        for k, v in csp.domains.items():
            if k not in current_assignment:
                print(f"  {k}: {v}")

    print_separator()
    print("CHOOSE VARIANT:")
    print("1. Predict the IMMEDIATE NEXT step/assignment.")
    print("2. Solve for the FINAL SOLUTION.")
    
    mode = get_int_input("Choice", 1)

    # --- Evaluation Phase ---

    if mode == 1:
        # Challenge: What happens next?
        print("\n--- QUESTION: PREDICT NEXT STEP ---")
        print(f"Based on the strategy (Tie-breaking: Alphabetical, Heuristic: {heuristic}),")
        print("which variable is assigned next, and what is its value?")
        print("(If the solver backtracks, enter 'BACKTRACK' for the variable name)")
        
        next_event, next_assign, _ = next_state
        
        if next_event == 'BACKTRACK':
            ans_var = input("Variable (or 'BACKTRACK'): ").strip().upper()
            if ans_var == 'BACKTRACK':
                print("✅ CORRECT! The solver hit a dead end and backtracked.")
            else:
                print(f"❌ INCORRECT. The solver actually BACKTRACKED here.")
        
        elif next_event == 'SOLUTION':
            print("✅ Trick Question! The current state was actually the final solution!")
            
        else:
            # It was a standard STEP assignment
            # Find the difference between current_assignment and next_assign
            newly_assigned_var = None
            newly_assigned_val = None
            for k, v in next_assign.items():
                if k not in current_assignment:
                    newly_assigned_var = k
                    newly_assigned_val = v
                    break
            
            user_var = input("Variable Name: ").strip().upper()
            user_val = get_value_input("Value", domain_type)
            
            if user_var == newly_assigned_var and user_val == newly_assigned_val:
                print("✅ CORRECT! Excellent tracing.")
            else:
                print(f"❌ INCORRECT.")
                print(f"The solver selected variable '{newly_assigned_var}' and assigned value '{newly_assigned_val}'.")
                if heuristic == 'MRV':
                     print("(Remember: MRV picks the variable with fewest remaining values in the CURRENT domains).")

    elif mode == 2:
        # Challenge: Solve the rest
        print("\n--- QUESTION: FINAL SOLUTION ---")
        print("Given the current partial assignment, complete the rest.")
        
        # Find the true final solution from history
        final_event, final_assign, _ = history[-1]
        
        if final_event != 'SOLUTION':
            # This path actually leads to failure
            print("Hint: This partial assignment might lead to a failure later...")
            user_guess = input("Enter 'FAIL' if you think it's unsolvable, or press Enter to guess values: ")
            if user_guess.upper() == 'FAIL':
                print("✅ CORRECT! This path leads to a backtrack/failure.")
            else:
                print("❌ It was actually a failing path (Result was None).")
        else:
            # Ask for every missing variable
            user_solution = current_assignment.copy()
            missing_vars = [v for v in csp.variables if v not in current_assignment]
            missing_vars.sort()
            
            print(f"Please assign values for: {', '.join(missing_vars)}")
            
            for var in missing_vars:
                # Use the new helper to get Int or String correctly
                val = get_value_input(f"{var} =", domain_type)
                user_solution[var] = val
            
            if user_solution == final_assign:
                print("✅ CORRECT! You found the solution.")
            else:
                print("❌ INCORRECT.")
                print(f"Your solution: {user_solution}")
                print(f"Actual solution: {final_assign}")

    # Show full history option
    print_separator()
    show_hist = input("Press Enter to exit, or type 'H' to see the full solver history: ").strip().upper()
    if show_hist == 'H':
        print("\n--- FULL SOLVER HISTORY ---")
        for i, (evt, asn, dom) in enumerate(history):
            print(f"Step {i+1}: {evt} | Assign: {asn}")

if __name__ == "__main__":
    main()
