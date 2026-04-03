import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="PPE Detection", layout="wide")

st.title("🦺 PPE Detection Dashboard")


st.sidebar.header("Settings")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5)

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# Function to draw bounding boxes
def draw_boxes(image, detections):
    draw = ImageDraw.Draw(image)

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = f"{det['class']} ({det['confidence']})"    
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        draw.text((x1, y1 - 10), label, fill="red")

    return image

if uploaded_file is not None:

    col1, col2 = st.columns(2)

    image = Image.open(uploaded_file)

    with col1:
        st.subheader("📷 Original Image")
        st.image(image, use_column_width=True)

    if st.button("🚀 Detect PPE"):
        files = {"file": uploaded_file.getvalue()}

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            files=files
        )

        result = response.json()

        detections = [
            d for d in result["detections"]
            if d["confidence"] >= confidence_threshold
        ]

        output_image = image.copy()
        output_image = draw_boxes(output_image, detections)

        with col2:
            st.subheader("🎯 Detection Result")
            st.image(output_image, use_column_width=True)

        # Metrics
        st.markdown("---")
        st.subheader("📊 Detection Summary")

        total = len(detections)
        helmets = sum(1 for d in detections if d["class"] == "helmet")
        vests = sum(1 for d in detections if d["class"] == "vest")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Objects", total)
        col2.metric("Helmets", helmets)
        col3.metric("Vests", vests)

        # Table view
        st.markdown("---")
        st.subheader("📋 Detailed Results")
        st.json(detections)

else:
    st.info("Upload an image to start detection 🚀")