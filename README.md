# 🧩 Rubik's Cube Solver

A Python application that uses your laptop camera to scan all 6 faces of a scrambled Rubik's Cube and provides a step-by-step solution algorithm.

---

## Features

- Live camera feed to capture each face of the cube
- Automatic colour detection and face mapping
- Cube state validation (ensures a legal, solvable configuration)
- Solution generation using an efficient solving algorithm
- Clear, human-readable move output (e.g. `U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2`)

---

## How It Works

1. **Scan** — Hold each of the 6 faces of your cube up to the camera one at a time. The app overlays a 3×3 grid to guide alignment.
2. **Detect** — Colour detection maps each of the 9 stickers per face to one of the 6 cube colours.
3. **Validate** — The app checks that the scanned state is a legal Rubik's Cube configuration.
4. **Solve** — A solving algorithm computes the solution and outputs the move sequence.

---

## Requirements

- Python 3.9+
- A working webcam

---

## Installation

```bash
git clone https://github.com/your-username/rubiks-cube-solver.git
cd rubiks-cube-solver
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py
```

Follow the on-screen prompts to scan each face in order:

| Step | Face   | Colour (standard orientation) |
|------|--------|-------------------------------|
| 1    | Top    | White                         |
| 2    | Front  | Green                         |
| 3    | Right  | Red                           |
| 4    | Bottom | Yellow                        |
| 5    | Back   | Blue                          |
| 6    | Left   | Orange                        |

Once all 6 faces are scanned, the solution will be printed to the terminal and displayed on screen.

---

## Libraries Used

### Computer Vision & Camera Input

| Library | Purpose |
|---|---|
| **OpenCV** (`opencv-python`) | Capturing the camera feed, drawing the grid overlay, and processing frames |
| **NumPy** | Array manipulation for image data and colour calculations |

### Colour Detection

| Library | Purpose |
|---|---|
| **OpenCV** (HSV colour space) | Converting frames to HSV to reliably detect sticker colours under varying lighting |
| **scikit-learn** (optional) | KMeans clustering as an alternative approach to identify the 6 dominant colours from a scan |

### Cube Solving

| Library | Purpose |
|---|---|
| **kociemba** | Implements Herbert Kociemba's two-phase algorithm — finds near-optimal solutions in 20 moves or fewer. This is the industry-standard approach used by most hobby cube solvers. |

### Interface (optional enhancements)

| Library | Purpose |
|---|---|
| **tkinter** | Simple GUI wrapper if you want a desktop window beyond the OpenCV preview |
| **rich** | Pretty terminal output for displaying the move sequence |

---

## Installing Dependencies

```bash
pip install opencv-python numpy kociemba scikit-learn rich
```

Or use the provided `requirements.txt`:

```
opencv-python>=4.8.0
numpy>=1.24.0
kociemba>=1.1.1
scikit-learn>=1.3.0
rich>=13.0.0
```

---

## Project Structure

```
rubiks-cube-solver/
│
├── project-research/         # Any research conducted related to the project
│
├── src/
│	├── main.py               # Entry point
│	├── scanner.py            # Camera feed and face scanning logic
│	├── colour_detector.py    # HSV-based sticker colour classification
│	├── cube_state.py         # Cube state representation and validation
│	├── solver.py             # Wrapper around the kociemba solver
│	├── display.py            # Overlay rendering and move output
│
├── requirements.txt
└── README.md
```

---

## Move Notation

Solutions are given in standard WCA (World Cube Association) notation:

| Symbol | Meaning |
|---|---|
| `U` | Up face clockwise |
| `D` | Down face clockwise |
| `L` | Left face clockwise |
| `R` | Right face clockwise |
| `F` | Front face clockwise |
| `B` | Back face clockwise |
| `X2` | Turn face X twice (180°) |
| `X'` | Turn face X counter-clockwise |

---

## Known Limitations

- Colour detection can struggle in poor or uneven lighting — a neutral background and consistent lighting is recommended
- Glossy or worn stickers may cause misreads; manual correction support is a planned feature
- Currently supports the standard 3×3×3 Rubik's Cube only
