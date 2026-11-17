# Connect 4 AI — Streamlit clone

A Streamlit Connect Four interface inspired by the supplied screenshot.

## Included
- `app.py`: Streamlit interface and session/game flow
- `engine.py`: 8-column x 6-row game engine, Minimax and Alpha-Beta pruning
- `requirements.txt`: Streamlit dependency

## Run

You already have Streamlit installed, so from this folder run:

```bash
streamlit run app.py
```

If dependencies are needed:

```bash
pip install -r requirements.txt
```

## Engine notes
The board uses the supplied 8 x 6 representation: `board[col][0]` is the
bottom cell. The original window-scoring weights are retained for depth-limited
leaf evaluation. Winner detection is separate from the heuristic score so
heuristic totals cannot accidentally masquerade as a win.

The screenshot visibly shows seven columns, whereas the supplied Python engine
specifies eight. This package preserves the supplied engine's 8-column board;
the UI is styled to match the screenshot, with eight drop controls accordingly.
