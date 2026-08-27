from memory import MemorySnapshot, format_snapshot


def test_format_snapshot():
    text = format_snapshot(MemorySnapshot(16000, 6000, 10000, 62.5))
    assert "62.5%" in text
    assert "Available: 6,000 MB" in text
