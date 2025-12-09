# AI-Project

Un mic proiect educațional care compară algoritmi pentru problema N-Queens și conține un placeholder pentru întrebări despre echilibrul Nash.

## Structură

- `main.py` – punct de intrare care apelează logica din pachetul `ai_project`.
- `ai_project/`
  - `cli.py` – fluxul principal al aplicației (parsarea întrebării și rutarea către solver).
  - `nqueens/` – algoritmii și utilitarele pentru problema N-Queens.
    - `algorithms/` – modulul pentru reprezentarea stării, algoritmii clasici (BFS/DFS/IDDFS), vizualizator, Simulated Annealing și MRV.
    - `experiment.py` – orchestrarea experimentelor și generarea răspunsului textual.
  - `nash/solver.py` – placeholder pentru logica de echilibru Nash.

## Rulare

```bash
python main.py
```

Introduceți o întrebare de forma:
- „Care e cel mai bun algoritm pentru n=8?”
- „Care este echilibrul Nash ...” (rutează către modulul Nash).