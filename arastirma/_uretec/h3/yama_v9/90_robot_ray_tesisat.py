"""Native GLB in/out wrapper; see robot_integrated_v21/run.py. No station edits."""
from pathlib import Path
import os,subprocess,sys

root=Path(__file__).resolve().parents[4]
if len(sys.argv)!=3:raise SystemExit('Usage: 90_robot_ray_tesisat.py input.glb output.glb')
source=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve()
subprocess.run([sys.executable,str(root/'arastirma/_uretec/robot_integrated_v21/run.py'),str(source),'--output',str(output)],cwd=root,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8'))
