from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz
import requests
from PIL import Image
import io
from app.process import predict_from_pil_image

app = FastAPI(title="Testing Kit Water Analyzer")

ESP32_IP = "192.168.1.100"  # Replace with your ESP32-CAM IP
ESP32_CAPTURE_ENDPOINT = f"http://{ESP32_IP}/capture"

@app.get("/analyze_kit")
async def analyze_kit():
    try:
        resp = requests.get(ESP32_CAPTURE_ENDPOINT, timeout=5)
        if resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"ESP32 returned status {resp.status_code}")
        pil_img = Image.open(io.BytesIO(resp.content)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch image from ESP32-CAM: {e}")

    try:
        results, overall_quality = predict_from_pil_image(pil_img)
        parameters = {k: v["value"] for k, v in results.items()}

        tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(tz)
        timestamp_str = now.strftime("%Y-%m-%d %I:%M %p %Z")

        return JSONResponse(content={
            "status": "success",
            "timestamp": timestamp_str,
            "parameters": parameters,
            "overall_quality": overall_quality
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
