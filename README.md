# AI Project

This project is a collection of solvers for classic Artificial Intelligence problems. It provides both a command-line interface (CLI) and a web-based user interface (UI) to interact with the solvers.

## Features

The project currently implements the following AI problems:

*   **N-Queens:** Compares the performance of different search algorithms (DFS, BFS, IDDFS, Simulated Annealing, and MRV) for solving the N-Queens problem.
*   **Nash Equilibrium:** A placeholder for solving Nash equilibrium problems.
*   **Minimax:** A placeholder for the Minimax algorithm.
*   **Constraint Satisfaction Problems (CSP):** A generic CSP solver.
*   **Graph Coloring:** Solves the graph coloring problem using the CSP solver.
*   **Knight's Tour:** Solves the Knight's Tour problem using backtracking and Warnsdorff's rule.
*   **Generalized Hanoi:** Solves the Tower of Hanoi problem.

## Project Structure

The project is organized into the following directories:

*   `ai_project/`: The main Python package containing the core logic.
    *   `cli.py`: The entry point for the command-line application.
    *   `ui/`: The Flask web application for the user interface.
        *   `app.py`: The main Flask application file.
        *   `templates/index.html`: The HTML template for the web UI.
    *   `nqueens/`: The N-Queens problem solver.
    *   `nash/`: The Nash Equilibrium problem solver.
    *   `minimax/`: The Minimax algorithm implementation.
    *   `csp/`: The generic CSP solver.
    *   `graph_coloring/`: The Graph Coloring problem solver.
    *   `knights_tour/`: The Knight's Tour problem solver.
    *   `hanoi/`: The Generalized Hanoi problem solver.
*   `Resources/`: Contains PDF documents with theory about the implemented AI problems.

## How to Run

There are two ways to run the project: through the command-line interface (CLI) or the web-based user interface (UI).

### Command-Line Interface (CLI)

To run the CLI, execute the following command in your terminal:

```bash
python -m ai_project.cli
```

### Web User Interface (UI)

To run the web UI, execute the following command in your terminal:

```bash
python -m ai_project.ui.app
```

Then, open your web browser and navigate to `http://127.0.0.1:5001`.

## Usage

### CLI

The CLI provides an interactive menu to choose the problem you want to solve. You can also use command-line arguments to solve a problem directly.

**Interactive Mode:**

```bash
python -m ai_project.cli
```

**Direct Execution:**

*   **N-Queens:**
    ```bash
    python -m ai_project.cli --problem nqueens --n 8
    ```
*   **Graph Coloring:**
    ```bash
    python -m ai_project.cli --problem graph-coloring --graph '{"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}' --colors 'red,green,blue'
    ```
*   **Knight's Tour:**
    ```bash
    python -m ai_project.cli --problem knights-tour --knights_tour_size 5
    ```
*   **Generalized Hanoi:**
    ```bash
    python -m ai_project.cli --problem hanoi --hanoi_disks 3
    ```

### Web UI

The web UI provides a user-friendly interface to solve the problems. Simply select the problem you want to solve from the dropdown menu, enter the required parameters, and click the "Solve" button.
