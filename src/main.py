# Coordinates the execution flow:
#   - triggers the scan sequence
#   - validates the output state
#   - calls the solver
#   - displays the step-by-step moves

import sys
from cube_state import CubeState
from scanner import CubeScanner

def main():
    cube_state = CubeState()

    scanner = CubeScanner(cube_state)

    scan_success = scanner.scan()
    if not scan_success:
        print("\nScanning aborted. Exiting program.")
        sys.exit(0)

    print("\nProcessing scanned cube faces...")


if __name__ == "__main__":
    main()