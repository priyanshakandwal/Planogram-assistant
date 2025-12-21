from ultralytics import YOLO
import numpy as np
import cv2
from typing import List, Dict, Tuple

# Load model once (VERY IMPORTANT)
model = YOLO("yolov8n.pt")


def detect_products(image_bytes: bytes) -> Tuple[List[Dict], tuple]:
    """
    Runs YOLO detection on an image.

    Returns:
    - detections: list of detected objects
    - image_shape: (height, width, channels)
    """

    # Convert bytes → numpy image
    np_img = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Invalid image file")

    height, width, channels = image.shape

    # Run YOLO
    results = model(image, verbose=False)[0]

    detections = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        confidence = float(box.conf[0])

        x1, y1, x2, y2 = map(float, box.xyxy[0])

        detections.append({
            "label": label,
            "confidence": round(confidence, 2),
            "bbox": [x1, y1, x2, y2]
        })

    return detections, image.shape
