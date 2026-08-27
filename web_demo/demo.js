import {bootPython} from './pyodide-helper.js';let py;const out=document.querySelector('#output'),run=document.querySelector('#run');async function init(){py=await bootPython(['memory.py'],`import sys,types
sys.modules['psutil']=types.ModuleType('psutil')`);run.disabled=false;show();}function show(){if(!py)return;py.globals.set('total',Number(document.querySelector('#total').value));py.globals.set('used',Number(document.querySelector('#used').value));try{out.textContent=String(py.runPython(`from memory import MemorySnapshot,format_snapshot
available=max(0,total-used)
pct=(used/total*100) if total else 0
format_snapshot(MemorySnapshot(int(total),int(available),int(used),float(pct)))`));}catch(e){out.textContent='Error: '+e.message;}}run.disabled=true;run.addEventListener('click',show);init().catch(()=>{});
