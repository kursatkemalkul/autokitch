"""Chain step 73; reuse the existing K implementation without duplication."""
from pathlib import Path
import os,sys,subprocess
root=Path(os.environ.get('YAMA_URETEC',Path(__file__).resolve().parents[2]))
script=root/'codex/k_montaj/73_k_tavan_baglantilari.py'
subprocess.run([sys.executable,str(script),*sys.argv[1:]],check=True)
