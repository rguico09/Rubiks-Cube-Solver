# Interfaces with the Python `kociemba` library
#   - converting our internal state representation into Kociemba's 54-character string notation
#   - triggering the solver
#   - and parsing the move sequence

import kociemba

class SolverError(Exception):
    pass

def solve_cube(cube_string):
    pass

def get_move_description(move):
    pass
