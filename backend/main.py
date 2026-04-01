from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
from ultralytics import YOLO

app = FastAPI()

model = YOLO("model/best.pt")
class_names = model.names

@app.get("/")
def home():
    return {"message": "PPE API running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    
    image_bytes = await file.read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    results = model(img)

    detections = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])

            if conf > 0.5:   # filter
                detections.append({
                    "class": class_names[cls],
                    "confidence": round(conf, 3),
                    "bbox": [round(x1,2), round(y1,2), round(x2,2), round(y2,2)]
                })

    return {"detections": detections}