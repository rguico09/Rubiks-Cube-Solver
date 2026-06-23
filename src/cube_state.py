# Houses:
#   - the internal state representation of the cube
#   - mappings between scans and validation logic
#       - (ensures exactly 9 of each color, valid edges/corners, and solvable permutation parity)

class CubeState:
    def __init__(self):
        # maps face names to list of 9 HSV tuples
        self.faces_raw = {
            'U': None,
            'F': None,
            'R': None,
            'D': None,
            'B': None,
            'L': None
        }
        
        # default HSV references for standard colors
        # fallback before centers are scanned
        self.default_references = {
            'U': (0, 10, 240),     # White (Low Saturation, High Value)
            'F': (60, 200, 180),   # Green
            'R': (2, 235, 190),    # Red
            'D': (30, 200, 200),   # Yellow
            'B': (115, 200, 180),  # Blue
            'L': (13, 230, 230)    # Orange
        }
        
        # human-readable face names for prompts
        self.scan_order = ['U', 'F', 'R', 'D', 'B', 'L']
        
        self.face_names_long = {
            'U': 'Top (White Center)',
            'F': 'Front (Green Center)',
            'R': 'Right (Red Center)',
            'D': 'Bottom (Yellow Center)',
            'B': 'Back (Blue Center)',
            'L': 'Left (Orange Center)'
        }

    def set_face_raw(self):
        pass

    def is_scan_complete(self):
        pass
    
    def get_current_references(self):
        pass

    def get_kociemba_string(self):
        pass

    def validate_state(self):
        pass

    def reset(self):
        pass
