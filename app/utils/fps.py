import time


class FPSCounter:
    """Measure elapsed processing time and frames per second."""

    def __init__(self) -> None:
        self.start_time: float | None = None
        self.end_time: float | None = None
        self.frames: int = 0

    def start(self) -> None:
        self.start_time = time.time()
        self.frames = 0

    def stop(self) -> None:
        self.end_time = time.time()

    def increment(self) -> None:
        self.frames += 1

    def elapsed(self) -> float:
        if self.start_time is None:
            return 0.0
        return (self.end_time or time.time()) - self.start_time

    def fps(self) -> float:
        elapsed_time = self.elapsed()
        return self.frames / elapsed_time if elapsed_time else 0.0
