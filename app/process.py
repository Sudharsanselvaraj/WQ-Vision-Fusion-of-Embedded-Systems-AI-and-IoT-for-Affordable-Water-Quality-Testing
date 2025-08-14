import os
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
from app.utils import denormalize, classify_status

# Parameters
PARAM_ORDER = ["Nitrate", "Nitrite", "Chlorine", "Hardness", "Carbonate", "pH"]
MODEL_DIR = os.path.join(os.getcwd(), "models")
IMG_SIZE = (128, 128)
EXPECTED_PADS = len(PARAM_ORDER)

# Load models
models = {}
for param in PARAM_ORDER:
    model_path = os.path.join(MODEL_DIR, f"{param}.h5")
    if os.path.exists(model_path):
        models[param] = tf.keras.models.load_model(model_path, compile=False)
    else:
        models[param] = None

def preprocess(img):
    img = cv2.resize(img, IMG_SIZE)
    img = img.astype("float32") / 255.0
    return np.expand_dims(img, axis=0)

def predict_from_pil_image(pil_img):
    img_np = np.array(pil_img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    h, w = img_bgr.shape[:2]
    box_width = w // EXPECTED_PADS
    boxes = [(i * box_width, 0, box_width, h) for i in range(EXPECTED_PADS)]

    results = {}
    for i, param in enumerate(PARAM_ORDER):
        x, y, ww, hh = boxes[i]
        crop = img_bgr[y:y+hh, x:x+ww]

        model = models.get(param)
        pred_val = None
        if model:
            inp = preprocess(crop)
            pred_val = float(model.predict(inp, verbose=0)[0][0])

        real_val = denormalize(param, pred_val)
        key_name = "Total Hardness" if param == "Hardness" else param
        results[key_name] = {"value": real_val}

    safe_count = sum(
        1 for param_name, v in results.items()
        if classify_status(param_name, v["value"]) == "safe"
    )
    perc = (safe_count / len(results)) * 100

    if perc >= 90:
        overall_quality = "Excellent"
    elif perc >= 70:
        overall_quality = "Good"
    elif perc >= 50:
        overall_quality = "Moderate"
    else:
        overall_quality = "Poor"

    return results, overall_quality
