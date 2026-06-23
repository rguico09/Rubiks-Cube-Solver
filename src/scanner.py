# Captures the laptop's camera feed using OpenCV (`cv2`)
# Renders a 3×3 grid overlay for sticker alignment
#   - and coordinates the scan sequence (directing the user to present faces in a specific order)

import cv2
import numpy as np
from colour_detector import get_roi_hsv, classify_sticker

class CubeScanner:
    def __init__(self, cube_state):
        self.cube_state = cube_state
        self.grid_size = 240
        self.cell_size = 80
        self.roi_size = 20
        self.current_step = 0
        self.validation_error_msg = None

        # RGB representation
        self.standard_rgbs = {
            'U': (245, 245, 245),        # white-ish
            'F': (0, 200, 0),            # green
            'R': (200, 0, 0),            # red
            'D': (220, 220, 0),          # yellow
            'B': (0, 0, 200),            # blue
            'L': (255, 130, 0),          # orange
        }

        # detailed instructions relative to "home" position
        #   - (green front, white top)
        self.rotation_guides = {
            'U': [
                "1. SCAN TOP FACE",
                "Home pos: Green front, White top.",
                "Tilt the cube DOWN so White is",
                "facing camera. Keep Green on bottom."
            ],
            'F': [
                "2. SCAN FRONT FACE",
                "Home pos: Green front, White top.",
                "Keep Green facing the camera,",
                "and White on top."
            ],
            'R': [
                "3. SCAN RIGHT FACE",
                "Home pos: Green front, White top.",
                "Turn the cube LEFT 90 degrees so",
                "Red faces camera. White on top."
            ],
            'D': [
                "4. SCAN BOTTOM FACE",
                "Home pos: Green front, White top.",
                "Tilt the cube UP so Yellow faces",
                "the camera. Keep Green on top."
            ],
            'B': [
                "5. SCAN BACK FACE",
                "Home pos: Green front, White top.",
                "Turn the cube 180 deg horizontally",
                "so Blue faces camera. White on top."
            ],
            'L': [
                "6. SCAN LEFT FACE",
                "Home pos: Green front, White top.",
                "Turn the cube RIGHT 90 degrees so",
                "Orange faces camera. White on top."
            ]
        }

    def get_roi_coordinates(self, width, height):
        # calculates coordinates of the 9 grid cells
        #   - based on frame size
        
        start_x = (width - self.grid_size) // 2
        start_y = (height - self.grid_size) // 2
        
        rois = []

        for r in range(3):
            for c in range(3):
                cx = start_x + (c * self.cell_size) + (self.cell_size // 2)
                cy = start_y + (r + self.cell_size) + (self.cell_size // 2)

                rx = cx - (self.roi_size // 2)
                ry = cy - (self.roi_size // 2)

                rois.append((rx, ry, self.roi_size, self.roi_size, cx, cy))

        return rois
    
    def check_running_counts(self):
        # checks the currently scanned facelets
        #   - to see if any colour already exceeds 9

        current_refs = self.cube_state.get_current_references()
        counts = {face: 0 for face in self.cube_state.scan_order}

        for face in self.cube_state.scan_order:
            if self.cube_state.faces_raw[face] is not None:
                for sticker_hsv in self.cube_state.faces_raw[face]:
                    char = classify_sticker(sticker_hsv, current_refs)
                    counts[char] += 1

        overlimits = [face for face, count in counts.items() if count > 9]
        if overlimits:
            names = [self.cube_state.face_names_long[o].split()[0] for o in overlimits]
            return True, f"Count limit exceeded for: {', '.join(names)}"
        
        return False, ""
    
    def review_and_edit_face(self, face, frozen_frame, rois):
        # enters a frozen review sub-loop
        #   - where the user can verify colours and edit them

        selected_idx = 0
        f_height, f_width = frozen_frame.shape[:2]
        sidebar_width = 240

        review_refs = self.cube_state.get_current_references()

        colour_keys = {
            ord('w'): 'U', ord('W'): 'U',
            ord('g'): 'U', ord('G'): 'F',
            ord('r'): 'U', ord('R'): 'R',
            ord('y'): 'U', ord('Y'): 'D',
            ord('b'): 'U', ord('B'): 'B',
            ord('o'): 'U', ord('O'): 'L',
        }

        colour_names_long = {
            'U': 'WHITE',
            'F': 'GREEN',
            'R': 'RED',
            'D': 'YELLOW',
            'B': 'BLUE',
            'L': 'ORANGE'
        }

        sticker_descs = [
            "Top-Left", "Top-Centre", "Top-Right",
            "Middle-Left", "Middle-Centre", "Middle-Right",
            "Bottom-Left", "Bottom-Centre", "Bottom-Right"
        ]

        while True:
            # create fresh canvas from frozen frame
            canvas = np.zeros((f_height, f_width + sidebar_width, 3), dtype=np.uint8)
            canvas[0:f_height, 0:f_width] = frozen_frame.copy()
            canvas[0:f_height, f_width:f_width + sidebar_width] = (30, 24, 24)

            # overlay current classification results
            # on top of the frozen cube frame
            classified_list = []

            for idx, (_, _, _, _, cx, cy) in enumerate(rois):
                sticker_hsv = self.cube_state.faces_raw[face][idx]
                classified_char = classify_sticker(sticker_hsv, review_refs)
                classified_list.append(classified_char)

                # draw colour overlay indicator
                colour_bgr = self.standard_rgbs[classified_char][::-1]
                cv2.rectangle(canvas, (cx - 15, cy - 15), (cx + 15, cy + 15), colour_bgr, -1)
                cv2.rectangle(canvas, (cx - 15, cy - 15), (cx + 15, cy + 15), (0, 0, 0), 1)

                # draw selection box if this is the highlighted sticker
                if idx == selected_idx:
                    start_x = (f_width - self.grid_size) // 2
                    start_y = (f_height - self.grid_size) // 2
                    
                    r_row = idx // 3
                    r_col = idx % 3

                    cell_x = start_x + (r_col * self.cell_size)
                    cell_y = start_y + (r_row * self.cell_size)

                    cv2.rectangle(canvas, (cell_x, cell_y), (cell_x + self,self.cell_size, cell_y + self.cell_size), (255, 0, 255), 3)

            # draw static grid outline
            start_x = (f_width - self.grid_size) // 2
            start_y = (f_height - self.grid_size) // 2
            cv2.rectangle(canvas, (start_x, start_y), (start_x + self.grid_size, start_y + self.grid_size), (0, 255, 0), 1)

            # draw review panel in sidebar
            cv2.putText(canvas, "STICKER REVIEW", (f_width + 20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            cv2.putText(canvas, self.cube_state.face_names_long[face].upper(), (f_width + 20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.standard_rgbs[face][::-1], 2)

            # shortcut instructions
            cv2.putText(canvas, "CONTROLS:", (f_width + 20, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            cv2.putText(canvas, "[1-9] : Select sticker", (f_width + 20, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
            cv2.putText(canvas, "W: White  | G: Green", (f_width + 20, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1)
            cv2.putText(canvas, "R: Red    | Y: Yellow", (f_width + 20, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1)
            cv2.putText(canvas, "B: Blue   | O: Orange", (f_width + 20, 185), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1)
            
            cv2.putText(canvas, "[ENTER] : Save & Continue", (f_width + 20, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
            cv2.putText(canvas, "[BACKSPACE] : Re-scan face", (f_width + 20, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 255), 1)

            cv2.line(canvas, (f_width + 10, 250), (f_width + sidebar_width - 10, 250), (100, 100, 100), 1)

            # selected sticker details
            sel_colour = classified_list[selected_idx]
            cv2.putText(canvas, "SELECTED STICKER:", (f_width + 20, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            cv2.putText(canvas, f"Sticker {selected_idx + 1} ({sticker_descs[selected_idx]})", (f_width + 20, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
            cv2.putText(canvas, f"Classified: {colour_names_long[sel_colour]}", (f_width + 20, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.standard_rgbs[sel_colour][::-1], 2)

            cv2.line(canvas, (f_width + 10, 335), (f_width + sidebar_width - 10, 335), (100, 100, 100), 1)

            # draw 3x3 layout of decisions
            preview_start_x = f_width + 75
            preview_start_y = 370
            preview_cell = 25

            cv2.putText(canvas, "CURRENT CLASSIFIED STATE:", (f_width + 20, 355), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)

            for r in range(3):
                for c in range(3):
                    idx = (r * 3) + c
                    char = classified_list[idx]
                    cell_bgr = self.standard_rgbs[char][::-1]
                    
                    px = preview_start_x + (c * preview_cell)
                    py = preview_start_y + (r * preview_cell)

                    cv2.rectangle(canvas, (px, py), (px + preview_cell - 2, py + preview_cell - 2), cell_bgr, -1)
                    border_color = (255, 0, 255) if idx == selected_idx else (100, 100, 100)
                    border_thickness = 2 if idx == selected_idx else 1
                    cv2.rectangle(canvas, (px, py), (px + preview_cell - 2, py + preview_cell - 2), border_color, border_thickness)

            # legend at bottom
            cv2.rectangle(canvas, (10, f_height - 35), (f_width - 10, f_height - 10), (0, 150, 150), -1)
            cv2.putText(canvas, "REVIEW ACTIVE: Enter to Save | Backspace to Re-scan | 1-9 to Select", (15, f_height - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

            cv2.imshow("Rubik's Cube Scanner", canvas)
            key = cv2.waitKey(1) & 0xFF
            
            cv2.imshow("Rubik's Cube Scanner", canvas)
            key = cv2.waitKey(1) & 0xFF

            if ord('1') <= key <= ord('9'):
                selected_idx = key - ord('1')
                print(f"Sticker {selected_idx + 1} selected.")
            elif key in colour_keys:
                target_face = colour_keys[key]
                target_hsv = review_refs[target_face]
                self.cube_state.faces_raw[face][selected_idx] = target_hsv
                print(f"Set Sticker {selected_idx + 1} to {colour_names_long[target_face]}.")
            elif key == 13 or key == 10:  # Enter
                print(f"Face {face} scan confirmed.")
                return True, False
            elif key == 8 or key == 127:  # Backspace
                print(f"Discarding current face {face} scan.")
                return False, False
            elif key == ord('q') or key == ord('Q') or key == 27:
                return False, True
            
    def scan(self):
        # opens the camera
        # displays the GUI
        # guides the user through scanning

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return False
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("\n=== Rubik's Cube Scanner Started ===")
        print("Use the OpenCV window. Keyboard controls:")
        print("  - [SPACE] to capture and review the current face")
        print("  - [1] to [6] to select/jump directly to a specific face to scan")
        print("  - [R] to go back to the previous face")
        print("  - [Q] to quit scanner")

        success = False
        self.current_step = 0
        self.validation_error_msg = None
        self.cube_state.reset()

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to read frame from camera.")
                break

            frame = cv2.flip(frame, 1)
            f_height, f_width = frame.shape[:2]

            # create layout canvas
            sidebar_width = 240
            canvas = np.zeros((f_height, f_width + sidebar_width, 3), dtype=np.uint8)
            canvas[0:f_height, 0:f_width] = frame
            canvas[0:f_height, f_width:f_width+sidebar_width] = (30, 24, 24)

            rois = self.get_roi_coordinates(f_width, f_height)

            live_hsv_list = []
            live_bgr_list = []
            for rx, ry, rw, rh, _, _ in rois:
                hsv = get_roi_hsv(frame, rx, ry, rw, rh)
                live_hsv_list.append(hsv)

                roi_bgr = frame[ry:ry + rh, rx:rx + rw]
                avg_bgr = cv2.mean(roi_bgr)[:3]
                live_bgr_list.append((int(avg_bgr[0]), int(avg_bgr[1]), int(avg_bgr[2])))

            # draw 3x3 overlay grid
            start_x = (f_width - self.grid_size) // 2
            start_y = (f_height - self.grid_size) // 2
            cv2.rectangle(canvas, (start_x, start_y), (start_x + self.grid_size, start_y + self.grid_size), (0, 255, 0), 2)

            for i in range(1, 3):
                cv2.line(canvas, (start_x + i * self.cell_size, start_y), (start_x + i * self.cell_size, start_y + self.grid_size), (0, 255, 0), 1)
                cv2.line(canvas, (start_x, start_y + i * self.cell_size), (start_x + self.grid_size, start_y + i * self.cell_size), (0, 255, 0), 1)

            for idx, (rx, ry, rw, rh, _, _) in enumerate(rois):
                thickness = 2 if idx == 4 else 1
                colour = (0, 0, 255) if idx == 4 else (255, 255, 0)
                cv2.rectangle(canvas, (rx, ry), (rx + rw, ry + rh), colour, thickness)

            # draw sidebar content
            current_face = self.cube_state.scan_order[self.current_step]

            cv2.putText(canvas, "RUBIK'S SOLVER", (f_width + 20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.line(canvas, (f_width + 10, 40), (f_width + sidebar_width - 10, 40), (100, 100, 100), 1)
            
            # rotation guide + dynamic warnings
            if self.validation_error_msg:
                cv2.putText(canvas, "COUNT ERROR!", (f_width + 20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                err_parts = self.validation_error_msg.split(';')
                for err_idx, part in enumerate(err_parts[:4]):
                    text = part.strip()
                    if len(text) > 28:
                        text = text[:25] + "..."
                    cv2.putText(canvas, text, (f_width + 20, 80 + err_idx * 14), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (100, 100, 255), 1)
            else:
                cv2.putText(canvas, "ROTATION GUIDE:", (f_width + 20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
                guide_lines = self.rotation_guides[current_face]
                cv2.putText(canvas, guide_lines[0], (f_width + 20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.standard_rgbs[current_face][::-1], 2)
                for l_idx, line in enumerate(guide_lines[1:], start=1):
                    cv2.putText(canvas, line, (f_width + 20, 80 + l_idx * 14), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (200, 200, 200), 1)
                
                # Check for running limits
                has_warn, _ = self.check_running_counts()
                if has_warn:
                    cv2.putText(canvas, "WARN: Count exceeded!", (f_width + 20, 134), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

            cv2.line(canvas, (f_width + 10, 140), (f_width + sidebar_width - 10, 140), (100, 100, 100), 1)

            # scan checklist progress
            cv2.putText(canvas, "SCAN PROGRESS:", (f_width + 20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)
            for idx, face in enumerate(self.cube_state.scan_order):
                y_pos = 185 + (idx * 19)
                colour = self.standard_rgbs[face][::-1]
                cv2.circle(canvas, (f_width + 30, y_pos - 4), 6, colour, -1)
                cv2.circle(canvas, (f_width + 30, y_pos - 4), 6, (100, 100, 100), 1)

                is_scanned = self.cube_state.faces_raw[face] is not None
                status_text = "[DONE]" if is_scanned else "[PENDING]"
                status_colour = (0, 255, 0) if is_scanned else (120, 120, 120)

                if idx == self.current_step:
                    cv2.putText(canvas, f"> {idx+1}. {face}", (f_width + 48, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
                else:
                    cv2.putText(canvas, f"  {idx+1}. {face}", (f_width + 48, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
                
                cv2.putText(canvas, status_text, (f_width + 120, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, status_colour, 1)

            cv2.line(canvas, (f_width + 10, 305), (f_width + sidebar_width - 10, 305), (100, 100, 100), 1)

            # live camera sensor colour boxes
            preview_start_x = f_width + 75
            preview_start_y = 345
            preview_cell = 25

            cv2.putText(canvas, "LIVE CAMERA SENSOR:", (f_width + 20, 325), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (180, 180, 180), 1)
            for r in range(3):
                for c in range(3):
                    idx = (r * 3) + c
                    cell_bgr = live_bgr_list[idx]
                    px = preview_start_x + (c * preview_cell)
                    py = preview_start_y + (r * preview_cell)
                    cv2.rectangle(canvas, (px, py), (px + preview_cell - 2, py + preview_cell - 2), cell_bgr, -1)
                    border_colour = (0, 0, 255) if idx == 4 else (100, 100, 100)
                    cv2.rectangle(canvas, (px, py), (px + preview_cell - 2, py + preview_cell - 2), border_colour, 1)

            # bottom legend
            if self.validation_error_msg:
                cv2.rectangle(canvas, (10, f_height - 35), (f_width - 10, f_height - 10), (0, 0, 255), -1) # Red highlight
                cv2.putText(canvas, "COUNT ERROR: Press 1-6 to select and re-scan face.", (20, f_height - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
            else:
                cv2.rectangle(canvas, (10, f_height - 35), (f_width - 10, f_height - 10), (0, 0, 0), -1)
                cv2.putText(canvas, "SPACE: Capture | R: Back | 1-6: Jump to Face | Q: Cancel", (15, f_height - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.43, (255, 255, 255), 1)

            cv2.imshow("Rubik's Cube Solver", canvas)
            key = cv2.waitKey(1) & 0xFF

            # direct face navigation shortcut
            if ord('1') <= key <= ord('6'):
                target_step = key - ord('1')
                self.current_step = target_step
                self.validation_error_msg = None
                print(f"Jumped directly to face {self.cube_state.scan_order[target_step]} ({self.cube_state.face_names_long[self.cube_state.scan_order[target_step]]})")

            # capture
            elif key == ord(' '):
                self.cube_state.set_face_raw(current_face, live_hsv_list)

                # enter reviewing and editing mode
                confirmed, abort = self.review_and_edit_face(current_face, frame, rois)
                if abort:
                    print("Scanning aborted during review.")
                    break
                elif confirmed:
                    self.validation_error_msg = None
                    if self.current_step < 5:
                        self.current_step += 1
                    else:
                        # scan is complete
                        # perform validation immediately
                        kociemba_string, _ = self.cube_state.get_kociemba_string()
                        is_valid, validation_msg = self.cube_state.validate_state(kociemba_string)
                        if is_valid:
                            print("All 6 faces successfully scanned and confirmed.")
                            success = True
                            break
                        else:
                            print(f"Sticker count validation failed: {validation_msg}")
                            # keep user at the last step but display error message
                            self.validation_error_msg = validation_msg
                else:
                    self.cube_state.faces_raw[current_face] = None
                    print(f"Rescanning face {self.cube_state.face_names_long[current_face]}...")

            # step back
            elif key == ord('r') or key == ord('R'):
                self.validation_error_msg = None
                if self.current_step > 0:
                    self.current_step -= 1
                    self.cube_state.faces_raw[self.cube_state.scan_order[self.current_step]] = None
                    print(f"Moved back. Ready to re-scan {self.cube_state.face_names_long[self.cube_state.scan_order[self.current_step]]}.")
                else:
                    self.cube_state.reset()
                    print("Scanner reset. Ready to scan Top face.")

            # abort
            elif key == ord('q') or key == ord('Q') or key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        for i in range(4):
            cv2.waitKey(i)

        return success
