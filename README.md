# 🦺 PPE Detection System

Production-ready Personal Protective Equipment (PPE) detection using YOLOv8, FastAPI, and OpenCV.

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.110%2B-brightgreen)](https://fastapi.tiangolo.com/)
[![YOLOv8](https://img.shields.io/badge/yolov8-ultralytics-orange)](https://github.com/ultralytics/ultralytics)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

A modern, scalable architecture for PPE detection on images and videos. Features a professional web UI, REST API, CLI support, Docker deployment, comprehensive logging, and full configuration management.

### Key Highlights

✨ **Modern Web UI** - Drag-and-drop interface with real-time results  
⚡ **REST API** - Image/video prediction endpoints  
🖥️ **CLI Support** - Command-line inference  
📦 **Modular Design** - Clean separation of concerns  
🐳 **Docker Ready** - Full containerization support  
📊 **Monitoring** - Structured logging and metrics  
🧪 **Tested** - Unit tests for core modules  

## Quick Start

### 1) Setup

```bash
cd /home/parth/Desktop/PPE-Detection
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run

```bash
python run.py
```

Visit: **http://127.0.0.1:8000** 🚀

---

## Features

### Web Dashboard

- **Drag-and-drop upload** for images and videos
- **Real-time preview** of uploaded content
- **Live confidence threshold** adjustment
- **Summary statistics** for detections
- **Detailed results** with bounding box coordinates
- **Model information** display
- **Responsive design** for desktop and mobile

### REST API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Web UI dashboard |
| `/health` | GET | Health check |
| `/model/info` | GET | Model configuration |
| `/predict/image` | POST | Detect PPE in image |
| `/predict/video` | POST | Detect PPE in video |

### CLI

```bash
# Image inference
python run.py --image sample.jpg --save

# Video inference
python run.py --video demo.mp4 --save --conf 0.35

# Webcam (placeholder)
python run.py --camera 0
```

---

## Project Structure

```
PPE-Detection/
├── app/
│   ├── api/               # FastAPI routes
│   ├── core/              # Config, logging, exceptions
│   ├── models/            # Model loading and detection
│   ├── services/          # Inference and drawing
│   ├── static/            # Web UI assets
│   │   ├── index.html     # Dashboard
│   │   ├── style.css      # Styling
│   │   └── app.js         # Client logic
│   ├── utils/             # Utilities (image, video, fps)
│   ├── constants.py       # App constants
│   └── schemas.py         # API response models
│
├── config.yaml            # Configuration
├── run.py                 # Server & CLI entrypoint
├── requirements.txt       # Dependencies
├── requirements-dev.txt   # Dev dependencies
│
├── weights/               # Model weights
├── input/                 # Uploaded files
├── output/                # Results
│   ├── images/            # Detected images
│   ├── videos/            # Detected videos
│   └── json/              # JSON outputs
├── logs/                  # Application logs
├── tests/                 # Unit tests
├── docs/                  # Documentation
│
├── Dockerfile             # Docker image
├── docker-compose.yml     # Docker Compose
├── INSTALLATION.md        # Detailed setup guide
├── README.md              # This file
└── LICENSE                # MIT License
```

---

## Installation & Setup

### Prerequisites

- Python 3.12+
- pip or conda
- Virtual environment (recommended)

### Full Setup Guide

See [INSTALLATION.md](INSTALLATION.md) for comprehensive instructions including:
- ✅ Environment setup
- ✅ Dependency installation
- ✅ Configuration
- ✅ Docker deployment
- ✅ Troubleshooting
- ✅ Performance optimization

### Quick Installation

```bash
# Clone/navigate to project
cd /home/parth/Desktop/PPE-Detection

# Create virtual environment (if needed)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run!
python run.py
```

---

## Usage

### Web Dashboard

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Open browser:**
   ```
   http://127.0.0.1:8000
   ```

3. **Upload image or video** via drag-and-drop or click

4. **Click "Detect PPE"** to run inference

5. **View results** with confidence scores and bounding boxes

### REST API

**Predict on image:**
```bash
curl -X POST "http://127.0.0.1:8000/predict/image" \
  -F "file=@sample.jpg"
```

**Predict on video:**
```bash
curl -X POST "http://127.0.0.1:8000/predict/video" \
  -F "file=@demo.mp4"
```

**Get model info:**
```bash
curl http://127.0.0.1:8000/model/info
```

### Command Line

```bash
# Single image
python run.py --image test_images/sample.jpg --save

# Video file
python run.py --video demo.mp4 --save

# Custom confidence
python run.py --image sample.jpg --conf 0.35

# Custom port
python run.py --port 9000
```

---

## Configuration

Edit `config.yaml` to customize detection behavior:

```yaml
model:
  path: weights/best.pt
  name: yolov8n
  device: cpu              # cpu or cuda
  confidence_threshold: 0.5
  iou_threshold: 0.45
  image_size: 640

output:
  output_dir: output
  image_dir: output/images
  video_dir: output/videos
  log_dir: logs

draw:
  font_scale: 0.5
  thickness: 2
  box_color: [0, 255, 0]
  text_color: [255, 255, 255]

api:
  host: 0.0.0.0
  port: 8000
```

---

## Docker

### Build & Run

```bash
docker compose up --build
```

### Access

```
http://127.0.0.1:8000
```

### Rebuild After Changes

```bash
docker compose up --build --force-recreate
```

---

## Testing

```bash
# Run all tests
pytest -q

# Run specific test file
pytest tests/test_settings.py -v

# With coverage
pytest --cov=app
```

---

## Architecture

### Core Modules

- **`app.core.settings`** - Configuration management with Pydantic
- **`app.core.logger`** - Structured logging setup
- **`app.core.exceptions`** - Custom exception classes

- **`app.models.model_loader`** - YOLO model loading
- **`app.models.detector`** - Detection logic

- **`app.services.inference`** - High-level inference engine
- **`app.services.drawing`** - Bounding box drawing

- **`app.utils.image_utils`** - Image I/O operations
- **`app.utils.video_utils`** - Video processing pipeline
- **`app.utils.fps`** - Performance metrics

- **`app.api.routes`** - FastAPI endpoints
- **`app.schemas`** - Pydantic response models

### Design Principles

✅ **Single Responsibility** - Each module has one clear purpose  
✅ **Modularity** - Easy to extend and reuse components  
✅ **Testability** - Dependency injection and clear interfaces  
✅ **Configuration** - Externalized settings via YAML  
✅ **Error Handling** - Custom exceptions with context  
✅ **Logging** - Structured logs to file and console  

---

## Performance

### Optimization Tips

1. **Reduce image size** in config.yaml:
   ```yaml
   image_size: 416  # Default: 640
   ```

2. **Increase confidence threshold**:
   ```yaml
   confidence_threshold: 0.6  # Default: 0.5
   ```

3. **Use GPU** (if available):
   ```yaml
   device: cuda
   ```

4. **Batch processing** for videos (frame skipping):
   - Modify `VideoProcessor.process()` to skip frames

### Benchmarks

- **Image (640x640)** on CPU: ~2-5 fps
- **Image (640x640)** on GPU: ~30-50 fps
- **Video (480p)** on CPU: ~1-2 fps
- **Video (480p)** on GPU: ~15-30 fps

*Varies by hardware and model size*

---

## Deployment

### Local Development

```bash
python run.py
```

### Production (Gunicorn + Uvicorn)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 run:create_app
```

### Cloud Platforms

- **Render**: Connect GitHub repo, set start command
- **Railway**: Deploy from Dockerfile
- **AWS**: ECS with ECR image
- **Azure**: Container Instances
- **DigitalOcean**: App Platform

See [INSTALLATION.md](INSTALLATION.md#production-deployment) for details.

---

## API Documentation

**Interactive Swagger UI**: http://127.0.0.1:8000/docs

**ReDoc**: http://127.0.0.1:8000/redoc

---

## Logging

Logs are written to `logs/ppe_detection.log` and console.

View logs:
```bash
tail -f logs/ppe_detection.log
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE)

---

## Acknowledgments

- **YOLOv8** - [Ultralytics](https://github.com/ultralytics/ultralytics)
- **FastAPI** - [Tiangolo](https://github.com/tiangolo/fastapi)
- **OpenCV** - [OpenCV Team](https://github.com/opencv/opencv)

---

## Support

For help:

1. **Check logs**: `logs/ppe_detection.log`
2. **Read docs**: [INSTALLATION.md](INSTALLATION.md)
3. **API docs**: http://127.0.0.1:8000/docs
4. **Config**: `config.yaml`

---

## Next Steps

- 🎯 Upload your first image at **http://127.0.0.1:8000**
- 📚 Read [INSTALLATION.md](INSTALLATION.md) for advanced setup
- 🔧 Customize `config.yaml` for your use case
- 🐳 Deploy with Docker to your favorite platform
- 🚀 Scale with Kubernetes or cloud services

---

**Happy detecting! 🦺**


