"""Terminal step93: compact outline wall and single internal QR customer column."""
from pathlib import Path
import os,subprocess,sys
root=Path(__file__).resolve().parents[4]
if len(sys.argv)!=3:raise SystemExit('Usage: 93_qr_duvar.py canonical_machine.glb output.glb')
subprocess.run([sys.executable,str(root/'arastirma/_uretec/robot_integrated_v24/run.py'),str(Path(sys.argv[1]).resolve()),'--output',str(Path(sys.argv[2]).resolve())],cwd=root,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8'))
