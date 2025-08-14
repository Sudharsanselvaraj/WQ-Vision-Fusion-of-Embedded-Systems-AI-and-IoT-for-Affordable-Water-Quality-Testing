from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import pytz
from PIL import Image
import io
import os
from app.process import predict_from_pil_image

app = FastAPI(title="Testing Kit Water Analyzer")

# Set your deployed domain here
BASE_URL = "https://wqvision-testing-kit.onrender.com"  # Change if needed

# Create images folder if it doesn't exist
os.makedirs("images", exist_ok=True)

# Mount static files (serve /images/* URLs from local images folder)
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.post("/analyze")
async def analyze_kit(request: Request):
    try:
        data = await request.body()
        if not data:
            raise HTTPException(status_code=400, detail="No image data received")

        pil_img = Image.open(io.BytesIO(data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image: {e}")

    try:
        results, overall_quality = predict_from_pil_image(pil_img)

        # Save image with timestamp
        tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(tz)
        timestamp_str = now.strftime("%Y-%m-%d %I:%M %p %Z")
        filename = now.strftime("%Y%m%d_%H%M%S") + ".jpg"
        save_path = os.path.join("images", filename)
        pil_img.save(save_path)

        # Build full image URL
        image_url = f"{BASE_URL}/images/{filename}"

        return JSONResponse(content={
            "status": "success",
            "timestamp": timestamp_str,
            "parameters": {k: v["value"] for k, v in results.items()},
            "overall_quality": overall_quality,
            "image_url": image_url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
