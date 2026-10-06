"""Reproducible step92, preserving the incoming station geometry. No git/UI side effects."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
ASSETS=ROOT/'otonom/hat3d/robot-integrated-v23'
LOCAL=ROOT/'_local/codex_robot_v23'

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path)
    p.add_argument('--output',type=Path)
    p.add_argument('--repeat',type=int,default=1)
    a=p.parse_args()
    source=a.source.resolve()
    node=os.environ.get('AUTOKITCH_NODE') or shutil.which('node')
    if not node:raise RuntimeError('Node.js required; set AUTOKITCH_NODE to its executable.')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',MACHINE_NATIVE=str(LOCAL/'published_with_qr.glb'))
    def call(args):subprocess.run(args,cwd=ROOT,env=env,check=True)
    cad=ASSETS/'rail_cad.json'
    step=ROOT/'_local/codex_robot_v22/igus_ZLW_20200_3000.stp'
    expected='2c6462714c47b7cfb665d1a7e579d27576ff2f4d923c7fbdf1cb4d82f892cd94'
    if hashlib.sha256(step.read_bytes()).hexdigest()!=expected:raise RuntimeError('Manufacturer STEP integrity mismatch')
    call([sys.executable,str(HERE/'floor_plan.py')])
    call([sys.executable,str(HERE/'route_audit.py')])
    if not cad.exists():call([sys.executable,str(HERE/'cad_rail.py')])
    if json.loads(cad.read_text())['source_step_sha256']!=expected:raise RuntimeError('Tessellation source mismatch')
    records=[]
    for _ in range(a.repeat):
        call([sys.executable,str(HERE/'clean_source.py'),str(source)])
        call([node,str(HERE/'prepare_published.mjs')])
        call([node,'--max-old-space-size=8192',str(HERE/'build.mjs')])
        call([node,str(HERE/'audit.mjs')])
        call([sys.executable,str(HERE/'geometry_audit.py')])
        record={}
        for f in [LOCAL/'source_cleaned.glb',LOCAL/'combined_native.glb',LOCAL/'combined_meshopt.glb',ASSETS/'hat3_robot_v23.glb.gz']:
            h=hashlib.sha256()
            with f.open('rb') as stream:
                for block in iter(lambda:stream.read(8*1024*1024),b''):h.update(block)
            record[f.name]={'sha256':h.hexdigest(),'bytes':f.stat().st_size}
        records.append(record)
    same=all(r==records[0] for r in records)
    proof={'step':92,'input':source.name,'runs':records,'byte_identical':same,'full_collision_certified':False}
    (ASSETS/'repeat_build.json').write_text(json.dumps(proof,indent=2),encoding='utf8')
    if not same:raise RuntimeError('Non-deterministic integration output')
    if a.output:
        output=a.output.resolve();output.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(LOCAL/'combined_native.glb',output)
    print(json.dumps({'step':92,'runs':a.repeat,'byte_identical':same}),flush=True)

if __name__=='__main__':main()
