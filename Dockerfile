FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system packages required by OpenCV and video processing
RUN apt-get update \
	 && apt-get install -y --no-install-recommends \
		 build-essential \
		 ca-certificates \
		 ffmpeg \
		 libglib2.0-0 \
		 libsm6 \
		 libxext6 \
		 libxrender1 \
		 libx11-6 \
		 libxcb1 \
		 libgl1 \
		 libxcb-keysyms1 \
		 libxcb-image0 \
		 libxcb-shm0 \
		 libxcb-icccm4 \
		 libxcb-render0 \
		 libxcb-render-util0 \
		 libxcb-xfixes0 \
		 libxcb-util1 \
		 libxcb-xinerama0 \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Ensure headless OpenCV is installed and non-headless is removed to avoid GUI deps
RUN pip install --no-cache-dir --force-reinstall opencv-python-headless>=4.9.0 \
	&& pip uninstall -y opencv-python || true

COPY . ./

RUN mkdir -p /app/output/images /app/output/videos /app/logs /app/input

EXPOSE 8000

CMD ["python", "run.py"]
