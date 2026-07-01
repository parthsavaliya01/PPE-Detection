import logging
from pathlib import Path

from .settings import AppConfig, load_config

config: AppConfig = load_config()


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "ppe_detection") -> logging.Logger:
    ensure_directory(config.output.log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(config.output.log_dir / "ppe_detection.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = get_logger()
