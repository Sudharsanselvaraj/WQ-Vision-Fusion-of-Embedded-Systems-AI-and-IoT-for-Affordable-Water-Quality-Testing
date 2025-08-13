import cv2
import numpy as np

# Denormalize normalized value to real-world parameter
def denormalize(param, normalized_val):
    ranges = {
        "Nitrate": (0, 250),       # ppm
        "Nitrite": (0, 10),
        "Chlorine": (0, 3.0),
        "Hardness": (0, 300),
        "Carbonate": (0, 300),
        "pH": (0, 14),
    }
    if param not in ranges or normalized_val is None:
        return None
    min_val, max_val = ranges[param]
    real_val = normalized_val * (max_val - min_val) + min_val
    return round(real_val, 3)

# Classify safe/caution/danger
def classify_status(param, value):
    if value is None:
        return "unknown"
    try:
        v = float(value)
    except Exception:
        return "unknown"

    if param.lower() == "ph":
        return "safe" if 6.5 <= v <= 8.5 else "caution"
    if param.lower() == "hardness":
        return "safe" if v < 150 else "caution" if v < 300 else "danger"
    if v <= 1:
        return "safe"
    if v <= 5:
        return "caution"
    return "danger"

