# Memory Monitor

A safe, cross-platform view of current memory usage. The old “RAM releaser” behavior was removed because trimming every process working set is intrusive and is not a general memory-optimization strategy.

```bash
pip install psutil
python main.py
```

---

## Live demo

**[Open the live demo](https://mateotrucco.github.io/memory_monitor/)**

Browser security prevents direct access to host processes, Registry/startup data or Windows shortcuts. The demo uses safe sample data and, where possible, the repository’s real pure helper logic.

## Repository setup

This separated repository also includes:

- MIT license
- project-specific `.gitignore`
- automated tests / CI
- GitHub Pages deployment for the demo
- `screenshots/` placeholder for portfolio images

The source files from the cleaned portfolio base were preserved unless a web-demo integration file had to be added.

