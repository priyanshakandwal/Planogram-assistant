from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from detect import detect_products
from intelligence import generate_recommendations



app = FastAPI()

# ✅ CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)):
    image_bytes = await image.read()

    detections, shape = detect_products(image_bytes)
    height = shape[0]

    recommendations = generate_recommendations(detections, height)

    return {
        "detections": detections,
        "recommendations": recommendations
    }
