"""Append compact shop to step94 robot/QR output; preserve all motion channels."""
from pathlib import Path
import sys,subprocess,os
root=Path(__file__).resolve().parents[4]
if len(sys.argv)!=3:raise SystemExit('Usage: 95_dukkan_yerlesim.py step94.glb output.glb')
subprocess.run([sys.executable,str(root/'arastirma/_uretec/robot_integrated_v26/run.py'),str(Path(sys.argv[1]).resolve()),'--output',str(Path(sys.argv[2]).resolve())],cwd=root,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
