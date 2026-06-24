# Interfaces with the Python `kociemba` library
#   - converting our internal state representation into Kociemba's 54-character string notation
#   - triggering the solver
#   - and parsing the move sequence

import kociemba

class SolverError(Exception):
    pass

def solve_cube(cube_string):
    # solves cube using kociemba's algorithm
    try:
        solution = kociemba.solve(cube_string)
        if not solution:
            return []
        return solution.split()
    except ValueError as e:
        error_msg = str(e)
        if "Error 1" in error_msg:
            msg = "There is an issue with the cube's facelets (not exactly 9 of each color or mismatched centers)."
        elif "Error 2" in error_msg:
            msg = "Some edge pieces are invalid or in impossible combinations."
        elif "Error 3" in error_msg:
            msg = "One edge piece is flipped incorrectly (edge orientation error)."
        elif "Error 4" in error_msg:
            msg = "Some corner pieces are invalid or in impossible combinations."
        elif "Error 5" in error_msg:
            msg = "One corner piece is twisted (corner orientation error)."
        elif "Error 6" in error_msg:
            msg = "Two corners are swapped or in an impossible arrangement (parity error)."
        elif "Error 7" in error_msg:
            msg = "Two edges are swapped or in an impossible arrangement (parity error)."
        elif "Error 8" in error_msg:
            msg = "General permutation/parity error. The cube state is physically impossible."
        else:
            msg = f"Kociemba solver error: {error_msg}"
        raise SolverError(msg)
    except Exception as e:
        raise SolverError(f"An unexpected error occurred during solving: {str(e)}")


def get_move_description(move):
    face_map = {
        'U': 'Top (Up)',
        'D': 'Bottom (Down)',
        'L': 'Left',
        'R': 'Right',
        'F': 'Front',
        'B': 'Back'
    }
    
    if len(move) == 1:
        return f"Rotate the {face_map[move[0]]} face 90° Clockwise"
    elif move.endswith("'"):
        return f"Rotate the {face_map[move[0]]} face 90° Counter-Clockwise"
    elif move.endswith("2"):
        return f"Rotate the {face_map[move[0]]} face 180° (Double turn)"
    
    return f"Move {move}"
