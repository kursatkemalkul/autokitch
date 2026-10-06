"""Terminal robot rendering step91; rebuilds from the last unchanged machine GLB."""
from pathlib import Path
import os,subprocess,sys
root=Path(__file__).resolve().parents[4]
if len(sys.argv)!=3:raise SystemExit('Usage: 91_robot_zemin_temiz.py machine.glb output.glb')
subprocess.run([sys.executable,str(root/'arastirma/_uretec/robot_integrated_v22/run.py'),str(Path(sys.argv[1]).resolve()),'--output',str(Path(sys.argv[2]).resolve())],cwd=root,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8'))
