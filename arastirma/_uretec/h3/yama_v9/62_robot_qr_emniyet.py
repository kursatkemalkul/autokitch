"""Step62 review layout. Does not assert manufacturing/safety release.
GLB -> GLB; requires exact step61 input. QR3x4 + native UR10e + locks.
"""
from pathlib import Path
import os,sys,shutil,subprocess,tempfile
HERE=Path(__file__).resolve().parent.parent.parent/'robot_safety_v1'
node=os.environ.get('AUTOKITCH_NODE') or shutil.which('node')
if not node:
    candidate=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
    if candidate.is_file():node=str(candidate)
if not node:raise RuntimeError('Node>=20 required')
gi,go=map(lambda p:Path(p).resolve(),sys.argv[1:3])
layout=go.with_name(go.stem+'.layout.glb')
subprocess.run([sys.executable,str(HERE/'build.py'),str(gi),str(layout)],check=True)
subprocess.run([node,str(HERE/'add_robot.mjs'),str(layout),str(go)],check=True)
subprocess.run([node,str(HERE/'reach_audit.mjs'),str(layout)],check=True)
subprocess.run([sys.executable,str(HERE/'mechanical_audit.py')],check=True)
subprocess.run([node,str(HERE/'audit.mjs')],check=True)
print('STEP62: review layout saved; production/safety release remains open.',flush=True)
os._exit(0)
