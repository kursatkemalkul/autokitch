"""Terminal94: integrated QR column, inward box turn and measured compact wall."""
from pathlib import Path
import os,subprocess,sys
root=Path(__file__).resolve().parents[4]
if len(sys.argv)!=3:raise SystemExit('Usage: 94_qr_donus.py canonical_machine.glb output.glb')
subprocess.run([sys.executable,str(root/'arastirma/_uretec/robot_integrated_v25/run.py'),str(Path(sys.argv[1]).resolve()),'--output',str(Path(sys.argv[2]).resolve())],cwd=root,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8'))
