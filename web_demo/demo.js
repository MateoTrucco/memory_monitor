import { bootPython, parsePythonJson } from './pyodide-helper.js';

let py;
let history = [];
const total = document.querySelector('#total');
const used = document.querySelector('#used');
const range = document.querySelector('#usedRange');
const out = document.querySelector('#output');
const run = document.querySelector('#run');
const metrics = document.querySelector('#memoryMetrics');
const meter = document.querySelector('#memoryMeter');

async function init() {
  py = await bootPython(['memory.py'], `import sys,types\nsys.modules['psutil']=types.ModuleType('psutil')`);
  run.disabled = false;
  show();
}

function show() {
  if (!py) return;
  const totalValue = Number(total.value);
  const usedValue = Number(used.value);
  py.globals.set('total', totalValue);
  py.globals.set('used', usedValue);
  try {
    const raw = py.runPython(`import json\nfrom memory import MemorySnapshot, classify_pressure, format_snapshot\nif total <= 0 or used < 0 or used > total: raise ValueError('used memory must be between zero and total memory')\navailable=total-used\npct=used/total*100\ns=MemorySnapshot(int(total),int(available),int(used),float(pct))\np=classify_pressure(pct)\njson.dumps({'formatted':format_snapshot(s),'available':int(available),'percent':round(pct,1),'level':p.level,'message':p.message})`);
    const data = parsePythonJson(raw);
    history = [...history.slice(-23), data.percent];
    metrics.innerHTML = `<div class="metric"><strong>${data.percent}%</strong><small>Used</small></div><div class="metric"><strong>${data.available.toLocaleString()}</strong><small>MB available</small></div><div class="metric"><strong>${data.level}</strong><small>Pressure</small></div>`;
    meter.style.width = `${data.percent}%`;
    out.textContent = `${data.formatted}\n\n${data.message}`;
    const max = Math.max(...history, 100);
    document.querySelector('#history').innerHTML = history.map((value) => `<span class="chart-bar" style="height:${Math.max(4, value / max * 100)}%" title="${value}%"></span>`).join('');
  } catch (error) {
    out.textContent = `Validation error: ${error.message}`;
  }
}

function syncRange() {
  range.max = Math.max(1, Number(total.value) || 1);
  range.value = Math.min(Number(used.value) || 0, Number(range.max));
}

range.addEventListener('input', () => { used.value = range.value; show(); });
total.addEventListener('input', () => { syncRange(); show(); });
used.addEventListener('input', () => { syncRange(); show(); });
run.disabled = true;
run.addEventListener('click', show);
document.querySelector('#sample').addEventListener('click', () => {
  used.value = Math.round(Number(total.value) * (0.38 + Math.random() * 0.57));
  syncRange();
  show();
});
syncRange();
init().catch(() => {});
