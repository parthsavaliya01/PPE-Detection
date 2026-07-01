from pathlib import Path

import pytest

from app.utils.image_utils import load_image
from app.core.exceptions import InvalidPathError


def test_load_image_missing_file_raises():
    with pytest.raises(InvalidPathError):
        load_image(Path("nonexistent.jpg"))
