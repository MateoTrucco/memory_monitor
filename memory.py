"""Memory metrics with no process manipulation."""

from __future__ import annotations

from dataclasses import dataclass
import math

import psutil


@dataclass(frozen=True, slots=True)
class MemorySnapshot:
    total_mb: int
    available_mb: int
    used_mb: int
    percent: float


@dataclass(frozen=True, slots=True)
class MemoryPressure:
    level: str
    message: str


def classify_pressure(percent: float) -> MemoryPressure:
    """Classify memory use without claiming to diagnose system performance."""
    value = float(percent)
    if not math.isfinite(value) or value < 0 or value > 100:
        raise ValueError("percent must be a finite number between 0 and 100")
    if value < 60:
        return MemoryPressure("comfortable", "Plenty of memory is currently available.")
    if value < 80:
        return MemoryPressure("moderate", "Memory use is noticeable but still within a common working range.")
    if value < 92:
        return MemoryPressure("high", "Heavy workloads may benefit from closing unused applications.")
    return MemoryPressure("critical", "Very little memory is available; responsiveness may be affected.")


def get_memory_snapshot() -> MemorySnapshot:
    memory = psutil.virtual_memory()
    divisor = 1024 * 1024
    return MemorySnapshot(
        total_mb=round(memory.total / divisor),
        available_mb=round(memory.available / divisor),
        used_mb=round(memory.used / divisor),
        percent=float(memory.percent),
    )


def format_snapshot(snapshot: MemorySnapshot) -> str:
    return (
        f"Used: {snapshot.used_mb:,} MB / {snapshot.total_mb:,} MB "
        f"({snapshot.percent:.1f}%) — Available: {snapshot.available_mb:,} MB"
    )
