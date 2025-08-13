from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pytz
from PIL import Image
import io
from app.process import predict_from_pil_image

app = FastAPI(title="Testing Kit Water Analyzer")

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

        tz = pytz.timezone("Asia/Kolkata")
        now = datetime.now(tz)
        timestamp_str = now.strftime("%Y-%m-%d %I:%M %p %Z")

        return JSONResponse(content={
            "status": "success",
            "timestamp": timestamp_str,
            "parameters": {k: v["value"] for k, v in results.items()},
            "overall_quality": overall_quality
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
