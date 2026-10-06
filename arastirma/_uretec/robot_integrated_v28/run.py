"""Animation-only step97; retain exact current machine/rail/QR/floor."""
from pathlib import Path
import subprocess,sys,json,os,shutil
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
NODE=os.environ.get('AUTOKITCH_NODE') or shutil.which('node') or 'C:/Users/Kemal/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
if not Path(NODE).is_file():raise RuntimeError('Set AUTOKITCH_NODE to installed Node executable')
def run(*args):subprocess.run([str(NODE),*[str(x) for x in args]],cwd=ROOT,check=True)
source=str(Path(sys.argv[1]).resolve()) if len(sys.argv)>1 else ROOT/'otonom/hat3d/robot-integrated-v27/hat3_robot_v27.glb.gz'
output=str(Path(sys.argv[2]).resolve()) if len(sys.argv)>2 else None
run(HERE/'plan.mjs','.7',str(3.141592653589793),'1.15')
run(HERE/'hulls.mjs')
subprocess.run([sys.executable,str(HERE/'hulls.py')],cwd=ROOT,check=True)
run(HERE/'collision.mjs');run(HERE/'speed.mjs')
audits=[]
for i in range(2):
    run(HERE/'build.mjs',source,*([output] if output else []))
    audits.append(json.loads((ROOT/'otonom/hat3d/robot-integrated-v28/build_audit.json').read_text()))
assert audits[0]['raw_web_sha256']==audits[1]['raw_web_sha256']
assert audits[0]['gzip_sha256']==audits[1]['gzip_sha256']
(ROOT/'otonom/hat3d/robot-integrated-v28/repeat_build.json').write_text(json.dumps({'step':97,'runs':audits,'byte_identical':True},indent=2))
