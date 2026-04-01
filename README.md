# 🦺 PPE Detection System (YOLOv8 + FastAPI + Streamlit)

An end-to-end AI-powered PPE (Personal Protective Equipment) detection system that identifies safety gear such as helmets, vests, gloves, and more from images. The system provides a REST API for inference and an interactive Streamlit dashboard for visualization.

---

## 🚀 Features

- 🔍 Object Detection using YOLOv8
- ⚡ FastAPI-based REST API for inference
- 🎨 Streamlit UI with bounding box visualization
- 📊 Detection summary (helmet, vest, total count)
- 🎯 Confidence threshold filtering
- 📦 Clean modular project structure

---

## 🧠 Tech Stack

- Python
- YOLOv8 (Ultralytics)
- FastAPI
- Streamlit
- OpenCV
- NumPy
- PIL

---

## 📁 Project Structure
ppe_detection_project/
│
├── backend/
│ ├── main.py # FastAPI backend
│ ├── model/
│ │ └── best.pt # Trained YOLO model
│ └── requirements.txt
│
├── frontend/
│ ├── app.py # Streamlit UI
│ └── requirements.txt
│
├── test_images/
│ └── sample.jpg
│
└── README.md



---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/ppe-detection.git
cd ppe-detection

### 1. Setup backend
cd backend
pip install -r requirements.txt

# run server
uvicorn main:app --reload

### 1. Setup Frontend
cd frontend
pip install -r requirements.txt


streamlit run app.py


# 🔥 Future Improvements
🎥 Real-time video detection
🚨 Safety violation alerts (missing PPE)
☁️ Cloud deployment (Render / AWS)
📱 Mobile-friendly UI
📈 Analytics dashboard


