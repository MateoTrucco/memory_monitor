import pytest

from memory import MemorySnapshot, classify_pressure, format_snapshot


def test_format_snapshot():
    text = format_snapshot(MemorySnapshot(16000, 6000, 10000, 62.5))
    assert "62.5%" in text
    assert "Available: 6,000 MB" in text


@pytest.mark.parametrize(
    ("percent", "level"),
    [(10, "comfortable"), (60, "moderate"), (80, "high"), (95, "critical")],
)
def test_pressure_classification(percent, level):
    assert classify_pressure(percent).level == level


def test_pressure_rejects_invalid_percentage():
    with pytest.raises(ValueError):
        classify_pressure(120)
