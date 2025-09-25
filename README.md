
# PCB Placement Solver (Final Visualization)

This version produces **plots that match the assignment style** with:
- Colored blocks for components (USB red, MCU blue, XTAL orange, MB purple).
- Labels inside components.
- Red dashed keepout zone (semi-transparent fill).
- Orange dashed crystal proximity circle.
- Grid background.

## 📦 Contents
- `solver.py` → Solver script (random + anneal).
- `placement.json` → Final placement result.
- `placement.png` → PNG visualization.
- `placement.svg` → SVG visualization (vector).

## 🚀 How to Run
```bash
python solver.py --mode anneal --iters 20000 --seed 42 --out placement.json --png placement.png --svg placement.svg
```

This generates outputs that look like the expected example in the assignment.
