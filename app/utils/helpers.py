from pathlib import Path
from typing import Any


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def to_json_serializable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    return value
