# PPE Detection - Getting Started Guide

## Complete Setup Instructions

### Step 1: Clone/Navigate to Project

```bash
cd /home/parth/Desktop/PPE-Detection
```

### Step 2: Activate Virtual Environment

```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies (First Time Only)

```bash
pip install -r requirements.txt
```

For development/testing:

```bash
pip install -r requirements-dev.txt
```

### Step 4: Add Your Model Weights

**IMPORTANT:** The app requires a trained YOLO model.

Place your trained model file at:

```bash
weights/best.pt
```

If your model has a different name, update `config.yaml`:

```yaml
model:
  path: weights/your_model_name.pt
```

### Step 5: Run the Application

#### Option A: Start the API Server

```bash
python run.py
```

The app will start at: **http://127.0.0.1:8000**

You'll see output like:

```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Option B: Use Command-Line Interface

**Detect in a single image:**

```bash
python run.py --image test_images/sample.jpg --save
```

Output will be saved to `output/images/`

**Detect in a video:**

```bash
python run.py --video test_videos/demo.mp4 --save
```

Output will be saved to `output/videos/`

**Custom confidence threshold:**

```bash
python run.py --image sample.jpg --conf 0.35 --save
```

#### Option C: Run with Docker

Build and run using Docker Compose:

```bash
docker compose up --build
```

The API will be available at: **http://127.0.0.1:8000**

---

## Using the Web UI

Once the server is running, visit:

### **http://127.0.0.1:8000**

### Features:

1. **Upload Panel**
   - Drag and drop images/videos
   - Or click to browse files

2. **Settings**
   - Adjust confidence threshold
   - Real-time updates

3. **Model Info**
   - View model configuration
   - Check device (CPU/GPU)

4. **Predictions**
   - Click "Detect PPE" button
   - View results in real-time
   - See bounding boxes and confidence scores

5. **Results**
   - Detailed detection list
   - Summary statistics
   - Output file path

---

## API Endpoints (for curl/Postman)

### Health Check

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{
  "status": "healthy",
  "message": "PPE Detection API is running."
}
```

### Model Information

```bash
curl http://127.0.0.1:8000/model/info
```

Response:

```json
{
  "model_path": "weights/best.pt",
  "device": "cpu",
  "confidence_threshold": 0.5,
  "iou_threshold": 0.45,
  "image_size": 640
}
```

### Predict on Image

```bash
curl -X POST "http://127.0.0.1:8000/predict/image" \
  -F "file=@test_images/sample.jpg"
```

Response:

```json
{
  "detections": {
    "boxes": [[100, 150, 200, 300], ...],
    "scores": [0.95, 0.87, ...],
    "classes": ["helmet", "vest", ...]
  },
  "output_path": "output/images/prediction_sample.jpg"
}
```

### Predict on Video

```bash
curl -X POST "http://127.0.0.1:8000/predict/video" \
  -F "file=@test_videos/demo.mp4"
```

Response:

```json
{
  "detections": "saved_video",
  "metrics": {
    "total_frames": 150,
    "processed_frames": 150,
    "average_fps": 25.5,
    "total_inference_time": 5.87
  },
  "output_path": "output/videos/prediction_demo.mp4"
}
```

---

## Configuration

Edit `config.yaml` to customize:

```yaml
model:
  path: weights/best.pt
  name: yolov8n
  device: cpu          # Change to 'cuda' for GPU
  confidence_threshold: 0.5
  iou_threshold: 0.45
  image_size: 640

output:
  output_dir: output
  image_dir: output/images
  video_dir: output/videos
  json_dir: output/json
  log_dir: logs

draw:
  font_scale: 0.5
  thickness: 2
  box_color: [0, 255, 0]      # BGR format
  text_color: [255, 255, 255]

api:
  host: 0.0.0.0
  port: 8000
```

---

## Environment Variables

Create a `.env` file to override config values:

```env
PPE_MODEL_DEVICE=cuda
PPE_MODEL_CONFIDENCE_THRESHOLD=0.35
PPE_API_PORT=9000
PPE_API_HOST=localhost
```

---

## Running Tests

```bash
pytest -q
```

Run specific test:

```bash
pytest tests/test_settings.py -v
```

---

## Directory Structure

After running the app, you'll see:

```
PPE-Detection/
├── weights/
│   └── best.pt              # Your model (add this)
├── input/                   # Uploaded files
├── output/
│   ├── images/              # Annotated images
│   ├── videos/              # Annotated videos
│   └── json/                # JSON predictions
├── logs/
│   └── ppe_detection.log    # Application logs
└── ...
```

---

## Troubleshooting

### "Model file not found"

**Solution:** Place your trained model at `weights/best.pt`

```bash
cp path/to/your/model.pt weights/best.pt
```

### "Port already in use"

**Solution:** Use a different port

```bash
python run.py --port 9000
```

Or modify `config.yaml`:

```yaml
api:
  port: 9000
```

### "CUDA not available"

**Solution:** Use CPU mode

```bash
python run.py --image sample.jpg
```

Or in `config.yaml`:

```yaml
model:
  device: cpu
```

### "Module not found"

**Solution:** Reinstall dependencies

```bash
pip install -r requirements.txt --force-reinstall
```

---

## Performance Optimization

### For GPU Support

1. Install CUDA-enabled PyTorch:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

2. Update `config.yaml`:

```yaml
model:
  device: cuda
```

### Reduce Inference Time

```yaml
model:
  image_size: 480           # Default: 640 (larger = slower)
  confidence_threshold: 0.6  # Higher = fewer predictions
```

---

## Docker Deployment

### Build Custom Image

```bash
docker build -t ppe-detection:latest .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -v $(pwd)/weights:/app/weights \
  -v $(pwd)/output:/app/output \
  ppe-detection:latest
```

### Docker Compose with GPU

Update `docker-compose.yml`:

```yaml
services:
  ppe-detection:
    ...
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Then run:

```bash
docker compose up --build
```

---

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 run:create_app
```

### Environment Setup

1. Create `.env` with production settings:

```env
PPE_MODEL_DEVICE=cuda
PPE_API_HOST=0.0.0.0
PPE_API_PORT=8000
```

2. Set up log rotation (logs/ppe_detection.log)

3. Configure reverse proxy (nginx, Apache)

---

## Next Steps

1. ✅ Place your trained model in `weights/best.pt`
2. ✅ Run `python run.py`
3. ✅ Open http://127.0.0.1:8000 in your browser
4. ✅ Upload images/videos for detection
5. ✅ View real-time results with bounding boxes

---

## Support

For issues, check:

- `logs/ppe_detection.log` - Application logs
- `config.yaml` - Configuration settings
- API documentation at `http://127.0.0.1:8000/docs` (Swagger UI)

---

Happy detecting! 🦺
