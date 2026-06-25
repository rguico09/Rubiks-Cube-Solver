# Processes pixel data within the 9 grid ROI (Regions of Interest) boxes
# Converts them to HSV (Hue, Saturation, Value) for stable detection
#   - and maps them to standard Rubik's cube colors

from typing import Optional
import cv2
import numpy as np

def get_roi_hsv(frame: np.ndarray, x: int, y: int, w: int, h: int) -> tuple[int, int, int]:
    # extracts the region of interest (ROI) from the frame
    # converts it to HSV
    # and returns the average H, S, and V values

    # crop ROI
    roi = frame[y:y+h, x:x+w]
    # convert BGR to HSV
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # calculate median/mean values to minimise noise
    mean_val = cv2.mean(hsv_roi)

    return (int(mean_val[0]), int(mean_val[1]), int(mean_val[2]))

def colour_distance(hsv1: tuple[int, int, int], hsv2: tuple[int, int, int]) -> float:
    # computes a weighted distance between 2 HSV colours
    # handles hue wrapping and white/low-saturation calibaration

    h1, s1, v1 = hsv1
    h2, s2, v2 = hsv2

    dh = min(abs(h1 - h2), 180 - abs(h1 - h2))
    ds = s1 - s2
    dv = v1 - v2

    # if either colour is very desaturated, Hue is unstable
    # in that case, we rely primarily on Saturation and Value
    if s1 < 60 or s2 < 60:
        return 0.1 * (dh ** 2) + 1.2 * (ds ** 2) + 1.0 * (dv ** 2)
    # if either colour is saturated, Hue is the most reliable identifier
    # so heavily weights Hue
    else:
        return 3.0 * (dh ** 2) + 0.5 * (ds ** 2) + 0.5 * (dv ** 2)

def classify_sticker(sticker_hsv: tuple[int, int, int], centre_references: dict[str, tuple[int, int, int]]) -> Optional[str]:
    # classifies a sticker's HSV value into one of the 6 faces
    #   - by finding the reference centre that has the minimum colour distance

    min_dist = float('inf')
    matched_face = None

    for face, ref_hsv in centre_references.items():
        dist = colour_distance(sticker_hsv, ref_hsv)
        if dist < min_dist:
            min_dist = dist
            matched_face = face

    return matched_face
