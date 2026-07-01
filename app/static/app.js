// DOM elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const videoPreview = document.getElementById('videoPreview');
const emptyState = document.getElementById('emptyState');
const predictBtn = document.getElementById('predictBtn');
const resultsList = document.getElementById('resultsList');
const loadingOverlay = document.getElementById('loadingOverlay');
const confidence = document.getElementById('confidence');
const confValue = document.getElementById('confValue');
const modelInfo = document.getElementById('modelInfo');

let currentFile = null;
let currentFileType = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadModelInfo();
    setupEventListeners();
});

function setupEventListeners() {
    // File upload
    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect();
        }
    });

    // Predict button
    predictBtn.addEventListener('click', predictPPE);

    // Confidence slider
    confidence.addEventListener('input', (e) => {
        confValue.textContent = parseFloat(e.target.value).toFixed(2);
    });
}

function handleFileSelect() {
    const file = fileInput.files[0];
    if (!file) return;

    currentFile = file;
    currentFileType = file.type.startsWith('image') ? 'image' : 'video';

    // Clear previous results
    resultsList.innerHTML = '';
    predictBtn.disabled = false;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        emptyState.style.display = 'none';
        if (currentFileType === 'image') {
            preview.src = e.target.result;
            preview.style.display = 'block';
            videoPreview.style.display = 'none';
        } else {
            videoPreview.src = e.target.result;
            videoPreview.style.display = 'block';
            preview.style.display = 'none';
        }
    };
    reader.readAsDataURL(file);
}

async function predictPPE() {
    if (!currentFile) return;

    showLoading(true);
    const formData = new FormData();
    formData.append('file', currentFile);

    try {
        const endpoint = currentFileType === 'image'
            ? '/predict/image'
            : '/predict/video';

        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Prediction error:', error);
        resultsList.innerHTML = `
            <div class="error-message">
                <strong>Error:</strong> ${error.message}
            </div>
        `;
    } finally {
        showLoading(false);
    }
}

function displayResults(data) {
    resultsList.innerHTML = '';

    if (currentFileType === 'video') {
        // Video results
        const metrics = data.metrics || {};
        resultsList.innerHTML = `
            <div class="success-message">
                <strong>✓ Video processed successfully!</strong>
            </div>
            <div class="results-summary">
                <div class="summary-stat">
                    <div class="label">Total Frames</div>
                    <div class="value">${metrics.total_frames || 0}</div>
                </div>
                <div class="summary-stat">
                    <div class="label">Avg FPS</div>
                    <div class="value">${(metrics.average_fps || 0).toFixed(1)}</div>
                </div>
                <div class="summary-stat">
                    <div class="label">Time</div>
                    <div class="value">${(metrics.total_inference_time || 0).toFixed(1)}s</div>
                </div>
            </div>
            <p><strong>Output saved to:</strong> ${data.output_path}</p>
        `;
        return;
    }

    // Image results
    const detections = data.detections || {};
    const boxes = detections.boxes || [];
    const scores = detections.scores || [];
    const classes = detections.classes || [];

    if (boxes.length === 0) {
        resultsList.innerHTML = `
            <div class="error-message">
                No PPE detected in the image.
            </div>
        `;
        return;
    }

    // Summary
    const stats = calculateStats(classes);
    const summaryHtml = `
        <div class="results-summary">
            <div class="summary-stat">
                <div class="label">Total Objects</div>
                <div class="value">${boxes.length}</div>
            </div>
            ${Object.entries(stats).map(([cls, count]) => `
                <div class="summary-stat">
                    <div class="label">${capitalize(cls)}</div>
                    <div class="value">${count}</div>
                </div>
            `).join('')}
        </div>
    `;

    resultsList.innerHTML = summaryHtml;

    // Detections
    boxes.forEach((box, idx) => {
        const conf = scores[idx];
        const className = classes[idx];

        // Filter by confidence
        if (conf < parseFloat(confidence.value)) return;

        const item = document.createElement('div');
        item.className = 'result-item';
        item.innerHTML = `
            <div>
                <span class="class-name">${capitalize(className)}</span>
                <span class="confidence">${(conf * 100).toFixed(1)}%</span>
            </div>
            <div class="coords">
                [${box.map(v => v.toFixed(0)).join(', ')}]
            </div>
        `;
        resultsList.appendChild(item);
    });

    // Output path
    const pathDiv = document.createElement('div');
    pathDiv.innerHTML = `<p><strong>Output:</strong> ${data.output_path}</p>`;
    resultsList.appendChild(pathDiv);
}

function calculateStats(classes) {
    const stats = {};
    classes.forEach(cls => {
        stats[cls] = (stats[cls] || 0) + 1;
    });
    return stats;
}

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

async function loadModelInfo() {
    try {
        const response = await fetch('/model/info');
        const data = await response.json();

        modelInfo.innerHTML = `
            <p><strong>Model:</strong> <span>${data.model_path}</span></p>
            <p><strong>Device:</strong> <span>${data.device}</span></p>
            <p><strong>Confidence:</strong> <span>${data.confidence_threshold}</span></p>
            <p><strong>IOU:</strong> <span>${data.iou_threshold}</span></p>
            <p><strong>Size:</strong> <span>${data.image_size}</span></p>
        `;
    } catch (error) {
        console.error('Failed to load model info:', error);
        modelInfo.innerHTML = '<p>Unable to load model info</p>';
    }
}

function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}
