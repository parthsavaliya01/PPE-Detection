from pathlib import Path
from typing import Tuple

import cv2

from app.core.exceptions import InvalidPathError


def load_image(image_path: Path) -> cv2.Mat:
    """Load an image from disk and return a numpy array."""

    if not image_path.exists():
        raise InvalidPathError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise InvalidPathError(f"Unable to read image: {image_path}")

    return image


def save_image(image: cv2.Mat, output_path: Path) -> bool:
    """Save an image to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    return cv2.imwrite(str(output_path), image)
