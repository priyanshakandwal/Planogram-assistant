from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import base64

from yolo_model import model
from intelligence import generate_recommendations
from draw_boxes import draw_boxes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)):
    # Read image
    contents = await image.read()
    np_img = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    h, w, _ = img.shape

    # YOLO inference
    results = model(img)[0]

    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = model.names[int(box.cls[0])]
        conf = float(box.conf[0])

        detections.append({
            "label": label,
            "confidence": conf,
            "bbox": [x1, y1, x2, y2],
            "y_center": (y1 + y2) / 2
        })

    # Draw bounding boxes
    annotated_img = draw_boxes(img, detections)

    # Generate tips
    tips = generate_recommendations(detections, h)

    # Encode image → Base64
    _, buffer = cv2.imencode(".jpg", annotated_img)
    img_base64 = base64.b64encode(buffer).decode("utf-8")

    return {
        "recommendations": tips,
        "image": img_base64
    }
