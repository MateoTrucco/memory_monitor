"""Cross-platform memory monitor GUI.

The previous version forced every Windows process to trim its working set. This
replacement only displays operating-system memory metrics.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from memory import format_snapshot, get_memory_snapshot


class MemoryMonitor(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Memory Monitor")
        self.geometry("520x190")
        self.resizable(True, False)
        self.value = tk.DoubleVar()
        self.message = tk.StringVar()
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="System memory", font=("TkDefaultFont", 16, "bold")).pack(anchor="w")
        ttk.Progressbar(frame, variable=self.value, maximum=100).pack(fill="x", pady=16)
        ttk.Label(frame, textvariable=self.message, wraplength=470).pack(anchor="w")
        ttk.Button(frame, text="Refresh", command=self.refresh).pack(anchor="e", pady=(14, 0))
        self.refresh()

    def refresh(self) -> None:
        snapshot = get_memory_snapshot()
        self.value.set(snapshot.percent)
        self.message.set(format_snapshot(snapshot))


if __name__ == "__main__":
    MemoryMonitor().mainloop()
