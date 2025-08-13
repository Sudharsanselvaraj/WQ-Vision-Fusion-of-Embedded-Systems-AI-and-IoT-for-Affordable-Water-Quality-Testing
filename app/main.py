from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz
from PIL import Image
import io
from app.process import predict_from_pil_image  # your existing prediction logic

app = FastAPI(title="Testing Kit Water Analyzer")

@app.post("/analyze_kit")
async def analyze_kit(request: Request):
    try:
        # Read raw JPEG bytes from ESP32
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="No image received")
        pil_img = Image.open(io.BytesIO(body)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read image: {e}")

    try:
        # Predict parameters
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
