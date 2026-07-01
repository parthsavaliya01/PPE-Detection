import numpy as np

from app.core.settings import load_config
from app.models.model_loader import ModelLoader
from app.services.inference import InferenceEngine


def test_model_loader_can_load_model():
    config = load_config()
    loader = ModelLoader(config)
    model = loader.get_model()
    assert model is not None


def test_inference_engine_predict_array_returns_result():
    config = load_config()
    engine = InferenceEngine(config)
    image = np.zeros((640, 640, 3), dtype=np.uint8)
    result = engine.predict_array(image)
    assert hasattr(result, "boxes")
    assert hasattr(result, "scores")
    assert hasattr(result, "classes")
