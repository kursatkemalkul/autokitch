"""Step96: append shop to final robot integration, retaining every animation."""
from pathlib import Path
import argparse,subprocess,os,sys,shutil,json,hashlib
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
A=ROOT/'otonom/hat3d/robot-integrated-v27'
p=argparse.ArgumentParser();p.add_argument('source',nargs='?',type=Path,default=ROOT/'otonom/hat3d/robot-integrated-v26/hat3_robot_v26.glb.gz');p.add_argument('--output',type=Path);p.add_argument('--repeat',type=int,default=1);args=p.parse_args()
node=os.environ.get('AUTOKITCH_NODE') or shutil.which('node')
if not node:raise RuntimeError('Set AUTOKITCH_NODE to installed Node executable')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8')
def call(cmd):subprocess.run(cmd,cwd=ROOT,env=env,check=True)
call([sys.executable,str(HERE/'plan.py')])
records=[]
for _ in range(args.repeat):
    call([node,str(HERE/'build.mjs'),str(args.source.resolve())]+([str(args.output.resolve())] if args.output else []))
    record=json.loads((A/'floor_build.json').read_text())
    records.append({k:record[k] for k in ['source_sha256','raw_web_sha256','raw_web_bytes','gzip_sha256','gzip_bytes']})
same=all(r==records[0] for r in records)
(A/'repeat_build.json').write_text(json.dumps({'step':96,'runs':records,'byte_identical':same},indent=2),encoding='utf8')
if not same:raise RuntimeError('Step96 is not deterministic')
call([node,str(HERE/'audit.mjs'),str(args.source.resolve())])
call([sys.executable,str(HERE/'route_check.py')])
print(json.dumps({'step':96,'runs':args.repeat,'byte_identical':same}),flush=True)
