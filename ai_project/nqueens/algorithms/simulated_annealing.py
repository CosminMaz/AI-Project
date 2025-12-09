import numpy as np
import time


def print_board(configuration):
    n = len(configuration)
    board = np.zeros((n, n), dtype=int)
    for col in range(n):
        row = configuration[col]
        board[row][col] = 1
    print(board)


def gauss_distib_value(x, mean, stdev, factor):
    return factor / stdev * 0.398942280401 * np.exp(-((x - mean) ** 2) / (2 * (stdev ** 2)))


#===========COD GENERAT CU CHATGPT-5=================
def fast_conflicts(candidate):
    n = len(candidate)
    main_diag = np.zeros(2 * n, dtype=int)
    sec_diag = np.zeros(2 * n, dtype=int)

    for col, row in enumerate(candidate):
        main_diag[row - col + n] += 1
        sec_diag[row + col] += 1

    # number of attacking pairs = sum(k choose 2) = k*(k-1)/2 for each diagonal
    total = (
        np.sum(main_diag * (main_diag - 1)) +
        np.sum(sec_diag * (sec_diag - 1))
    ) // 2
    return total


def simulated_annealing(n, T, min_temp, decay):

    start_total = time.time()

    # FUNCTII MAI LENTE, ECHIVALENTE
    # def conflicts(candidate):
    #     total = 0
    #     for i in range(n):
    #         for j in range(i + 1, n):
    #             if abs(candidate[i] - candidate[j]) == abs(i - j):
    #                 total += 1
    #     return total

    # def pick_random_neighbor(candidate):
    #     i, j = np.random.choice(candidate.size, 2, replace=False)
    #     neighbor = candidate.copy()
    #     neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    #     return neighbor



    def heuristic(candidate):
        return -fast_conflicts(candidate)


    def pick_biased_neighbor(candidate):
        n = len(candidate)
        neighbor = candidate.copy()

        # compute diagonal occupancy
        main_diag = np.zeros(2 * n, dtype=int)
        sec_diag = np.zeros(2 * n, dtype=int)
        for col, row in enumerate(candidate):
            main_diag[row - col + n] += 1
            sec_diag[row + col] += 1

        # find queens in conflict
        conflicted_cols = []
        for col, row in enumerate(candidate):
            if main_diag[row - col + n] > 1 or sec_diag[row + col] > 1:
                conflicted_cols.append(col)

        if not conflicted_cols:
            return neighbor  # already conflict-free

        # pick one conflicted queen
        col = np.random.choice(conflicted_cols)
        swap_col = np.random.randint(0, n)
        while swap_col == col:
            swap_col = np.random.randint(0, n)

        # swap their positions
        neighbor[col], neighbor[swap_col] = neighbor[swap_col], neighbor[col]
        return neighbor
    #===========COD GENERAT CU CHATGPT-5=================


    
    candidate = np.random.permutation(n)
    h_candidate = heuristic(candidate)

    best_solution = candidate.copy()
    h_best_solution = h_candidate

    step = 0
    while T > min_temp:
        neighbor = pick_biased_neighbor(candidate)
        h_neighbor = heuristic(neighbor)

        if h_neighbor > h_candidate or np.random.uniform(0, 1) < np.exp(-abs(h_neighbor - h_candidate) / T):
            candidate = neighbor
            h_candidate = h_neighbor

        if h_candidate > h_best_solution:
            best_solution = candidate.copy()
            h_best_solution = h_candidate
            if h_best_solution == 0:
                end_total = time.time()
                runtime = end_total - start_total
                print(f"[SA] Solutie optima gasita la pasul {step}: {best_solution}")
                print(f"runtime: {runtime}")
                return best_solution 

        #T = gauss_distib_value(step, mean, stdev, factor)
        T*=decay
        step += 1

    end_total = time.time()
    runtime = end_total - start_total
    print(f"runtime la final executie: {runtime}, solutia cea mai buna dar cu defecte are {fast_conflicts(best_solution)} conflicte")
    return best_solution


#===main===

if __name__ == "__main__":
    N_input = input("Dimensiunea tablei (ex: 8): ").strip()
    N = int(N_input) if N_input != "" else 8

    print("\n--- Simulated Annealing ---")
    sol_sa = simulated_annealing(N, T=0.01, min_temp = 1e-30, decay = 0.9995)# pt N < 3000
    print_board(sol_sa)


