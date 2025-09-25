# PCB Placement Solver

This project implements an **automatic PCB component placement solver**. It uses:  
- **Random constructive initialization**  
- **Simulated annealing optimization**  

It ensures placement of components such as **USB, MCU, Crystal, and Mounting Brackets**, while respecting:  
- Edge alignment constraints  
- Crystal proximity constraints  
- Keep-out zones  
- Center-of-mass balance  

---

## ✨ Features
- Two solver modes: **Random** (baseline) and **Anneal** (optimization)  
- JSON output of final placements  
- Visual assignment-style output:  
  - Colored blocks with labels  
  - Dashed red keep-out zones  
  - Dashed orange crystal proximity circles  
  - Grid background  

---

## 🛠 How It Works

The solver operates in two stages:

1. **Random Constructive Initialization**  
   - Place all components randomly within the board.  
   - Respect hard constraints (edges, keep-outs, crystal proximity).  
   - Serves as a feasible starting point.

2. **Simulated Annealing Optimization**  
   - Iteratively swap or move components to improve score.  
   - Accept worse placements with a probability decreasing over time to escape local minima.  
   - Objective: minimize bounding box size and center-of-mass deviation.

Initial Random Placement
┌──────────────────────┐
│ USB MCU Crystal │
│ [ ] [ ] [ ] │
│ ... │
└──────────────────────┘
↓ Annealing
Optimized Placement
┌──────────────────────┐
│ USB MCU Crystal │
│ [ ] [ ] [ ] │
│ ... │
└──────────────────────┘

yaml
Copy code

---

## 📂 Package Contents
- `solver.py` → main solver script (CLI)  
- `placement.json` → example solver output (final placement + score + metadata)  
- `placement.png` → visualization of the placement  
- `placement.svg` → vector version of the visualization  
- `README.md` → this file  

---

## 🚀 Usage

### Random Baseline Solver
```bash
python solver.py --mode random --seed 42 --out placement.json --png placement.png
Simulated Annealing Optimization
bash
Copy code
python solver.py --mode anneal --iters 20000 --seed 123 --out placement.json --png placement.png --svg placement.svg
Options
--mode {random,anneal} → choose solver type

--iters N → number of iterations (only in anneal mode)

--seed N → random seed for reproducibility

--out FILE → output JSON file

--png FILE / --svg FILE → save placement plot

--show → display plot interactively

🧮 Scoring
The solver maximizes a score based on:

Compactness (smaller bounding box area is better)

Center-of-mass closeness to the board center

Simulated annealing gradually refines placements to improve the score.

⚙️ Requirements
Python 3.7+

matplotlib

Install requirements:

bash
Copy code
pip install matplotlib
📜 License
This project is for academic/educational purposes as part of the PCB placement assignment.
