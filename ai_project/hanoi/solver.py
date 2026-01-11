def hanoi_solver(n, source, destination, auxiliary):
    """
    Solves the Tower of Hanoi puzzle recursively and returns the steps.

    Args:
        n (int): The number of disks to move.
        source (str): The name of the source peg.
        destination (str): The name of the destination peg.
        auxiliary (str): The name of the auxiliary peg.

    Returns:
        list: A list of tuples, where each tuple represents a move
              (disk, source, destination).
    """
    moves = []
    if n == 1:
        moves.append((1, source, destination))
        return moves
    
    moves.extend(hanoi_solver(n - 1, source, auxiliary, destination))
    moves.append((n, source, destination))
    moves.extend(hanoi_solver(n - 1, auxiliary, destination, source))
    
    return moves

def solve_hanoi(n_disks):
    """
    Entry point for solving the Tower of Hanoi problem.

    Args:
        n_disks (int): The number of disks.

    Returns:
        str: A message containing the solution or an error message.
    """
    if n_disks < 1:
        return "Numărul de discuri trebuie să fie cel puțin 1."

    moves = hanoi_solver(n_disks, 'A', 'C', 'B')
    
    formatted_moves = "\n".join([f"- Mută discul {disk} de la {src} la {dest}" for disk, src, dest in moves])
    
    return f"Soluție pentru Turnurile din Hanoi cu {n_disks} discuri:\n\n{formatted_moves}"