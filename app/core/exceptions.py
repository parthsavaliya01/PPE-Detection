from typing import Any


class PPEException(Exception):
    """Base exception for PPE detection application."""

    def __init__(self, message: str, details: Any | None = None):
        super().__init__(message)
        self.details = details


class InvalidPathError(PPEException):
    """Raised when the supplied file or directory path is invalid."""


class ModelLoadError(PPEException):
    """Raised when the model cannot be loaded."""


class InferenceError(PPEException):
    """Raised when inference fails or returns an invalid result."""


class VideoProcessingError(PPEException):
    """Raised when video capture or saving fails."""
