# 🚀 Getting Started - PPE Detection System

Welcome! This is your complete guide to running the **production-ready PPE Detection System**.

---

## ⚡ 60-Second Quick Start

```bash
# 1. Navigate to project
cd /home/parth/Desktop/PPE-Detection

# 2. Activate environment
source .venv/bin/activate

# 3. Run the app
python run.py

# 4. Open browser
# http://127.0.0.1:8000
```

Done! 🎉

---

## 📋 Prerequisites

- ✅ Python 3.12+ (already installed)
- ✅ Virtual environment (already created: `.venv/`)
- ✅ Dependencies (already installed)
- ✅ Model weights (already present: `weights/best.pt` - 6.2 MB)

---

## 🔍 Verify Setup

Before running, verify everything is ready:

```bash
python verify.py
```

Expected output:
```
✅ All checks passed! (6/6)
```

---

## 🎯 Three Ways to Use

### Option 1: Web Dashboard (Recommended for Testing)

**Best for:** Visual testing, single file uploads

```bash
# Start server
python run.py

# Open browser
http://127.0.0.1:8000
```

**Features:**
- Drag-and-drop upload
- Real-time preview
- Adjustable confidence threshold
- Summary statistics
- Download results

### Option 2: REST API (Recommended for Integration)

**Best for:** Integrating with other systems

```bash
# Start server
python run.py

# In another terminal, upload image
curl -X POST "http://127.0.0.1:8000/predict/image" \
  -F "file=@test_image.jpg"

# Response: JSON with detections
```

**Available endpoints:**
- `GET /health` - Health check
- `GET /model/info` - Model configuration
- `POST /predict/image` - Detect in image
- `POST /predict/video` - Detect in video
- `GET /docs` - Interactive API docs

### Option 3: Command Line (Recommended for Batch Processing)

**Best for:** Processing multiple files

```bash
# Single image
python run.py --image sample.jpg --save

# Video file
python run.py --video demo.mp4 --save

# Custom confidence
python run.py --image sample.jpg --conf 0.35 --save

# Custom port
python run.py --port 9000
```

**Output:**
- Results saved to `output/images/` or `output/videos/`
- Logs written to `logs/ppe_detection.log`

---

## 📁 Output Directory Structure

After running predictions, you'll find:

```
output/
├── images/
│   └── prediction_sample.jpg          # Annotated image
├── videos/
│   └── prediction_demo.mp4            # Annotated video
└── json/
    └── prediction_sample.json         # Detection results (JSON)

logs/
└── ppe_detection.log                  # Application logs
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize behavior:

### Model Settings

```yaml
model:
  path: weights/best.pt           # Model file location
  device: cpu                     # cpu or cuda (if GPU available)
  confidence_threshold: 0.5       # Only show detections above this
  iou_threshold: 0.45             # Intersection over Union threshold
  image_size: 640                 # Input size (smaller = faster)
```

### Output Directories

```yaml
output:
  output_dir: output
  image_dir: output/images
  video_dir: output/videos
  json_dir: output/json
  log_dir: logs
```

### Drawing Settings

```yaml
draw:
  font_scale: 0.5                 # Label font size
  thickness: 2                    # Bounding box thickness
  box_color: [0, 255, 0]          # Box color (BGR)
  text_color: [255, 255, 255]     # Text color (BGR)
```

### API Settings

```yaml
api:
  host: 0.0.0.0                   # Bind address
  port: 8000                      # Port number
```

---

## 🐳 Docker

Run in Docker (isolated, no dependencies needed):

```bash
# Build and run
docker compose up --build

# The app will be at http://127.0.0.1:8000
```

---

## 📊 Viewing Results

### Web UI Results

1. Go to http://127.0.0.1:8000
2. Upload an image
3. Click "Detect PPE"
4. View results in right panel

### File Results

**Image predictions:**
```
output/images/prediction_*.jpg     # Annotated image
```

**Video predictions:**
```
output/videos/prediction_*.mp4     # Annotated video
```

**API JSON response:**
```json
{
  "detections": {
    "boxes": [[x1, y1, x2, y2], ...],
    "scores": [0.95, 0.87, ...],
    "classes": ["helmet", "vest", ...]
  },
  "output_path": "output/images/prediction_sample.jpg"
}
```

---

## 🔧 Troubleshooting

### "Address already in use"

Port 8000 is taken. Use a different port:

```bash
python run.py --port 9000
```

### "Model file not found"

Ensure `weights/best.pt` exists:

```bash
ls -lh weights/best.pt
```

If missing:
```bash
cp your_model.pt weights/best.pt
```

### "Permission denied"

Make scripts executable:

```bash
chmod +x run.py verify.py
```

### "No module named..."

Reinstall dependencies:

```bash
pip install -r requirements.txt --force-reinstall
```

### "CUDA not found"

Using GPU mode but CUDA not installed. Switch to CPU:

Edit `config.yaml`:
```yaml
model:
  device: cpu
```

### "Low FPS on video"

Reduce image size in `config.yaml`:

```yaml
model:
  image_size: 416        # Was 640
```

---

## 📈 Performance Tips

### Speed Up Inference

```yaml
model:
  image_size: 416            # Smaller = faster (accuracy trade-off)
  confidence_threshold: 0.6  # Higher = fewer predictions
```

### Use GPU (if available)

```yaml
model:
  device: cuda               # Must have CUDA installed
```

### Reduce Logs

Edit `app/core/logger.py`:
```python
logger.setLevel(logging.WARNING)  # Less verbose
```

---

## 🧪 Testing

Run automated tests:

```bash
# All tests
pytest -q

# Specific test
pytest tests/test_settings.py -v

# With coverage
pytest --cov=app tests/
```

---

## 📚 Documentation

Full documentation available in:

- **README.md** - Project overview
- **INSTALLATION.md** - Detailed setup guide
- **PROJECT_SUMMARY.md** - Architecture details
- **This file** - Quick start guide

---

## 💡 Example Workflows

### Example 1: Test Single Image

```bash
# 1. Run app
python run.py &

# 2. Upload via API
curl -X POST "http://127.0.0.1:8000/predict/image" \
  -F "file=@test.jpg" > results.json

# 3. View results
cat results.json | python -m json.tool
```

### Example 2: Batch Process Videos

```bash
# Process all videos in folder
for video in videos/*.mp4; do
  python run.py --video "$video" --save
done

# Results in output/videos/
ls output/videos/prediction_*.mp4
```

### Example 3: Web Dashboard

```bash
# 1. Start server
python run.py

# 2. Open browser to http://127.0.0.1:8000

# 3. Upload files via drag-and-drop

# 4. View results in real-time
```

### Example 4: Docker Deployment

```bash
# 1. Build image
docker compose build

# 2. Run container
docker compose up

# 3. Use API
curl -X POST "http://127.0.0.1:8000/predict/image" \
  -F "file=@test.jpg"
```

---

## 🎓 Understanding the Output

### Detection Results Breakdown

```json
{
  "detections": {
    "boxes": [
      [100.5, 150.2, 250.3, 400.8],    // [x1, y1, x2, y2] in pixels
      [300.1, 200.5, 450.2, 500.3]
    ],
    "scores": [
      0.95,                             // 95% confidence
      0.87                              // 87% confidence
    ],
    "classes": [
      "helmet",                         // Detected class
      "vest"                            // Detected class
    ]
  }
}
```

### Summary Statistics

- **Total Objects**: Count of all detections
- **Helmets**: Count of helmet detections
- **Vests**: Count of vest detections
- **Avg FPS**: Frames per second (video only)

---

## 🚀 Next Steps

1. ✅ Run `python run.py`
2. ✅ Open http://127.0.0.1:8000
3. ✅ Upload an image or video
4. ✅ View detections
5. ✅ Explore API at http://127.0.0.1:8000/docs
6. ✅ Check output in `output/` folder
7. ✅ Review logs in `logs/ppe_detection.log`

---

## 📞 Need Help?

1. **Run verification**: `python verify.py`
2. **Check logs**: `tail -f logs/ppe_detection.log`
3. **Read docs**: Open `README.md` or `INSTALLATION.md`
4. **API help**: Visit http://127.0.0.1:8000/docs
5. **Config help**: Review `config.yaml` and comments

---

## ✨ You're All Set!

Your PPE Detection System is **production-ready** and can handle:

- ✅ Real-time image detection
- ✅ Video processing
- ✅ REST API requests
- ✅ Docker deployment
- ✅ Batch processing
- ✅ Performance monitoring

**Start detecting now!** 🎉

```bash
python run.py
```

Then open: **http://127.0.0.1:8000**

---

Happy detecting! 🦺
