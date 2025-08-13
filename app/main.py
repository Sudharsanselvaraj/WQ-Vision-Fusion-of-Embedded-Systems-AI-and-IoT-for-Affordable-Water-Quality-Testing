from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from app.process import predict_from_pil_image
from PIL import Image
import io
from datetime import datetime
import pytz

app = FastAPI(title="Testing Kit Water Analyzer")

@app.post("/analyze_kit")
async def analyze_kit(file: UploadFile = File(...)):
    try:
        pil_img = Image.open(io.BytesIO(await file.read())).convert("RGB")
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
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
