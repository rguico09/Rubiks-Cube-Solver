# Coordinates the execution flow:
#   - triggers the scan sequence
#   - validates the output state
#   - calls the solver
#   - displays the step-by-step moves

import sys
from cube_state import CubeState
from scanner import CubeScanner
from solver import solve_cube, SolverError
from display import print_welcome, print_solution, print_validation_status

def main() -> None:
    print_welcome()

    cube_state = CubeState()

    scanner = CubeScanner(cube_state)

    scan_success = scanner.scan()
    if not scan_success:
        print("\nScanning aborted. Exiting program.")
        sys.exit(0)

    print("\nProcessing scanned cube faces...")

    # generate Kociemba 54-char string representation
    try:
        kociemba_string, _ = cube_state.get_kociemba_string()
    except Exception as e:
        print_validation_status(False, f"Failed to compute cube state: {str(e)}")
        sys.exit(1)
        
    # validate the generated state
    is_valid, validation_msg = cube_state.validate_state(kociemba_string)
    print_validation_status(is_valid, validation_msg)
    
    if not is_valid:
        print("Because the color counts are incorrect, the solver cannot run.")
        print("This is usually caused by lighting reflection or shadows during scanning.")
        sys.exit(1)
        
    # attempt to solve the cube
    print("Computing solving steps using Kociemba's two-phase algorithm...")
    try:
        solution_moves = solve_cube(kociemba_string)
        print_solution(solution_moves)
    except SolverError as se:
        print_validation_status(False, f"Solvability Error: {str(se)}")
        print("\nTip: Ensure the cube was scanned in standard orientation:")
        print("  1. Up    -> White center on top")
        print("  2. Front -> Green center facing you")
        print("  3. Right -> Red center facing right")
        print("  4. Down  -> Yellow center on bottom")
        print("  5. Back  -> Blue center facing away")
        print("  6. Left  -> Orange center facing left")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred while running the solver: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
