import os
import io
from datetime import datetime
import pytz
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from app.process import predict_from_pil_image

# Ensure received_images directory exists
os.makedirs("received_images", exist_ok=True)

app = FastAPI(title="Testing Kit Water Analyzer")

# Your deployed domain (change if different)
BASE_URL = "https://wqvision-testing-kit.onrender.com"

# Serve images directory as static files
app.mount("/images", StaticFiles(directory="received_images"), name="images")

@app.post("/analyze")
async def analyze_kit(request: Request):
    try:
        # Read raw image bytes
        data = await request.body()
        if not data:
            raise HTTPException(status_code=400, detail="No image data received")

        # Save image with timestamp filename
        tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(tz)
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp_str}.jpg"
        filepath = os.path.join("received_images", filename)

        with open(filepath, "wb") as f:
            f.write(data)

        # Open image for processing
        pil_img = Image.open(io.BytesIO(data)).convert("RGB")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    try:
        # Run prediction
        results, overall_quality = predict_from_pil_image(pil_img)

        # Format readable timestamp for response
        human_time = now.strftime("%Y-%m-%d %I:%M %p %Z")

        # Build full image URL
        full_image_url = f"{BASE_URL}/images/{filename}"

        return JSONResponse(content={
            "status": "success",
            "timestamp": human_time,
            "parameters": {k: v["value"] for k, v in results.items()},
            "overall_quality": overall_quality,
            "image_url": full_image_url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
