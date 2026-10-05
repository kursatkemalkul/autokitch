from pathlib import Path
import subprocess,shutil
ROOT=Path(__file__).resolve().parents[3]
node=shutil.which('node')
if not node:
 node=str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
subprocess.run([node,'--max-old-space-size=8192','arastirma/_uretec/robot_integrated_v18/prepare_published.mjs'],cwd=ROOT,check=True)
