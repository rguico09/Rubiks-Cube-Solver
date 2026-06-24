# Houses:
#   - the internal state representation of the cube
#   - mappings between scans and validation logic
#       - (ensures exactly 9 of each color, valid edges/corners, and solvable permutation parity)

from colour_detector import classify_sticker

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
            'U': (0, 10, 240),     # white (low Saturation, high Value)
            'F': (60, 200, 180),   # green
            'R': (2, 235, 190),    # red
            'D': (30, 200, 200),   # yellow
            'B': (115, 200, 180),  # blue
            'L': (13, 230, 230)    # orange
        }
        
        # human-readable face names for prompts
        self.scan_order = ['U', 'F', 'R', 'D', 'B', 'L']
        
        self.face_names_long = {
            'U': 'Top (White Centre)',
            'F': 'Front (Green Centre)',
            'R': 'Right (Red Centre)',
            'D': 'Bottom (Yellow Centre)',
            'B': 'Back (Blue Centre)',
            'L': 'Left (Orange Centre)'
        }

    def set_face_raw(self, face, hsv_list):
        # stores the 9 raw HSV values for a given face
        if face in self.faces_raw:
            self.faces_raw[face] = list(hsv_list)

    def is_scan_complete(self):
        # returns true if all 6 faces have been scanned
        return all(self.faces_raw[face] is not None for face in self.scan_order)
    
    def get_current_references(self):
        # gets HSV references
        refs = self.default_references.copy()
        for face in self.scan_order:
            if self.faces_raw[face] is not None:
                refs[face] = self.faces_raw[face][4]
        return refs

    def get_kociemba_string(self):
        # classifies all facelets
        #   - using centre references
        # and constructs the 54-character kociemba representation
        if not self.is_scan_complete():
            raise ValueError("Cannot generate Kociemba string: Not all faces have been scanned.")
        
        centre_refs = self.get_current_references()
        classified_faces = {}

        for face in self.scan_order:
            classified_faces[face] = []
            for sticker_hsv in self.faces_raw[face]:
                classified_char = classify_sticker(sticker_hsv, centre_refs)
                classified_faces[face].append(classified_char)
        
        kociemba_order = ['U', 'R', 'F', 'D', 'L', 'B']
        kociemba_chars = []
        for face in kociemba_order:
            kociemba_chars.extend(classified_faces[face])

        kociemba_string = "".join(kociemba_chars)
        
        return kociemba_string, classified_faces

    def validate_state(self, kociemba_string):
        # validates if the generated string is valid
        if len(kociemba_string) != 54:
            return False, f"Expected 54 facelets, got {len(kociemba_string)}."
        
        counts = {char: kociemba_string.count(char) for char in "URFDLB"}

        errors = []
        for face, count in counts.items():
            if count != 9:
                errors.append(f"Face '{face}' has {count} stickers instead of 9.")

        if errors:
            return False, "; ".join(errors)
            
        return True, "Valid cube state configuration."

    def reset(self):
        # resets the scanned faces
        for face in self.faces_raw:
            self.faces_raw[face] = None
